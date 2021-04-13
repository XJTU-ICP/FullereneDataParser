# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : csi.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import os
import re
from multiprocessing import Pool, RLock, freeze_support

import numpy as np
import pandas as pd
from fullerenedatapraser.io.recursion import recursion_files
from fullerenedatapraser.io.xyz import simple_read_xyz_xtb
from fullerenedatapraser.molecular.fullerene import FullereneFamily
from fullerenedatapraser.util.logger import Logger
from fullerenedatapraser.util.mp import print_error
from tqdm import tqdm

logger = Logger(__name__, console_on=True)


def calculate_csi(fullerene: FullereneFamily):
    """

    Parameters
    ----------
    fullerene:FullereneFamily
        molecule Instance of Fullerene.
    Returns
    -------
        CSI
    References
    ----------
    Wang, Y., Díaz-Tendero, S., Alcamí, M., & Martín, F. (2018).
    Topology-Based Approach to Predict Relative Stabilities of Charged and Functionalized Fullerenes.
    Journal of Chemical Theory and Computation, 14(3), 1791–1810. https://doi.org/10.1021/acs.jctc.7b01048
    """

    assert fullerene.natoms % 2 == 0, f"Not A classical Fullerene. Check your input atoms: {fullerene}."
    chi = np.linalg.eigh(fullerene.atomADJ)[:fullerene.natoms // 2]
    return chi[0], chi[1]


def store_csi(adj_path, xyz_dir, target_path):
    """
    save file to `target_path`,{
    csi_list,spiral_num,energy
    }
    Parameters
    ----------
    adj_path:
        ADJfile path by using `data.spiral.adj_store`
    xyz_dir:
        .xyz files directory
    target_path
        .npz file path to store information

    See Also
    --------
    data.spiral.adj_store

    """
    spiral_num_list = []
    csi_list = []
    energy_list = []
    pa = re.compile("[0-9]+")
    pbar = tqdm(total=len(os.listdir(xyz_dir)))
    for xyz_path in recursion_files(rootpath=xyz_dir, ignore_mode=True):
        pbar.set_description(f'{adj_path}')
        pbar.update()
        f = list(simple_read_xyz_xtb(xyz_path))[-1]

        spiral_num = int(pa.findall(os.path.splitext(xyz_path)[0])[-1])
        ADJ = pd.read_hdf(adj_path)
        atomadj = np.array(ADJ[ADJ["spiral_num"] == spiral_num]["atomadj"])[0]
        circleadj = np.array(ADJ[ADJ["spiral_num"] == spiral_num]["circleadj"])[0]
        energy = f.info["energy"]
        fuller = FullereneFamily(spiral=spiral_num, atomADJ=atomadj, circleADJ=circleadj, atoms=f)
        spiral_num_list.append(spiral_num)
        csi_list.append(calculate_csi(fuller)[0])
        energy_list.append(energy)
    np.savez(target_path, csi_list=csi_list, spiral_num=np.array(spiral_num_list), energy=np.array(energy_list))


def _store_csi(args):
    logger.debug(f"_store_csi:{args}")
    atomfile, circlefile, targetfile = args
    store_csi(atomfile, circlefile, targetfile)


def mp_store_csi(adj_dir, xyz_root_dir, target_dir):
    """
    Batch process of calculating CSI
    Parameters
    ----------
    adj_path
    xyz_dir
    target_path

    Returns
    -------

    """
    freeze_support()
    tqdm.set_lock(RLock())
    pa = re.compile("[0-9]+")
    po = Pool(4, initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
    for adj_path in recursion_files(adj_dir, format=""):
        # update = lambda *args: pbar.update()
        basename = "C" + pa.findall(os.path.splitext(adj_path)[0])[-1]
        xyz_dir = os.path.join(xyz_root_dir, basename)
        try:
            target_path = os.path.join(target_dir, basename + "_CSI.npz")
            args = adj_path, xyz_dir, target_path
            po.apply_async(func=_store_csi, args=(args,), error_callback=print_error)
        except FileNotFoundError:
            continue
    po.close()
    po.join()


if __name__ == '__main__':
    store_csi(adj_path=r"C:\Work\CODE\DATA\test\ADJ50.h5", xyz_dir=r"C:\Work\CODE\DATA\fullerxTBcal\xTBcal\C50", target_path=r"C:\Work\CODE\DATA\CSI\C50_CSI.npz")