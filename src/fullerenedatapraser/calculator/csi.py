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
from fullerenedatapraser.data.spiral import adj_gener
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


def store_csi(atomfile, circlefile, xyz_dir, target_path):
    """
    save file to `target_path`,{
    csi_list,spiral_num,energy
    }
    Parameters
    ----------
    atomfile
    circlefile
    xyz_dir:
        .xyz files directory
    target_path
        .npz file path to store information

    See Also
    --------
    data.spiral.adj_store, calculate_csi

    """
    spiral_num_list = []
    csi_list = []
    energy_list = []
    pa = re.compile("[0-9]+")
    pbar = tqdm(total=len(os.listdir(xyz_dir)))
    adjgener = adj_gener(atomfile, circlefile)
    for xyz_path in recursion_files(rootpath=xyz_dir, ignore_mode=True):
        adj = next(adjgener)
        pbar.set_description(f'{xyz_path}')
        pbar.update()
        f = list(simple_read_xyz_xtb(xyz_path))[-1]

        spiral_num = int(pa.findall(os.path.splitext(xyz_path)[0])[-1])
        assert spiral_num == adj["spiral_num"]
        atomadj = adj["atomadj"]
        circleadj = adj["circleadj"]
        energy = f.info["energy"]
        fuller = FullereneFamily(spiral=spiral_num, atomADJ=atomadj, circleADJ=circleadj, atoms=f)
        spiral_num_list.append(spiral_num)
        csi_list.append(calculate_csi(fuller)[0])
        energy_list.append(energy)
    np.savez(target_path, csi_list=csi_list, spiral_num=np.array(spiral_num_list), energy=np.array(energy_list))


def _store_csi(args):
    logger.debug(f"_store_csi:{args}")
    atomfile, circlefile, xyz_dir, target_path = args
    store_csi(atomfile, circlefile, xyz_dir, target_path)


def mp_store_csi(atomdir, circledir, xyz_root_dir, target_dir):
    """
    Batch process of calculating CSI

    See Also
    --------
    `store_csi`, `calculate_csi`

    """
    freeze_support()
    tqdm.set_lock(RLock())
    pa = re.compile("[0-9]+")
    po = Pool(1, initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
    for atomfile in recursion_files(atomdir, format=""):
        basename = os.path.basename(atomfile)
        circlefile = os.path.join(circledir, basename)

        # update = lambda *args: pbar.update()
        basename = "C" + pa.findall(os.path.splitext(atomfile)[0])[-1]
        xyz_dir = os.path.join(xyz_root_dir, basename)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        try:
            target_path = os.path.join(target_dir, basename + "_CSI.npz")
            args = atomfile, circlefile, xyz_dir, target_path
            po.apply_async(func=_store_csi, args=(args,), error_callback=print_error)
        except FileNotFoundError:
            continue
    po.close()
    po.join()

