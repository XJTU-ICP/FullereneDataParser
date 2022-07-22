# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : extend_csi.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : csi.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import logging
import os
import re
from multiprocessing import Pool, RLock, freeze_support
import pathlib

import numpy as np
from fullerenedataparser.data.spiral import adj_gener
from fullerenedataparser.io.recursion import recursion_files
from fullerenedataparser.io.xyz import simple_read_xyz_xtb
from fullerenedataparser.molecular.fullerene import FullereneFamily
from fullerenedataparser.util.config import setGlobValue
from fullerenedataparser.util.logger import Logger
from fullerenedataparser.util.mp import print_error
from fullerenedataparser.util.geometry import sphere_center_of_four_points
from tqdm import tqdm

setGlobValue("log_level", logging.DEBUG)
logger = Logger(__name__, console_on=True)


def calculate_ext_csi(fullerene: FullereneFamily, para=7, distance_cutoff=None):
    """
    Implemention of extended
    Parameters
    ----------
    fullerene:FullereneFamily
        molecule Instance of Fullerene.
    para:int
        multiple value to adj
    distance_cutoff: float or None
        distance more than cutoff will be regard as 0
    Returns
    -------
        CSI
    References
    ----------

    """

    assert fullerene.natoms % 2 == 0, f"Not A classical Fullerene. Check your input atoms: {fullerene}."
    assert fullerene.info["charge"] % 2 == 0, f"Only Deal with Even number charged Fullerene Now. Got charge:{fullerene.info['charge']}."
    # csi_adj = fullerene.atomADJ # not used actually

    distances = fullerene.get_all_distances()
    mask = np.ones_like(distances) - np.eye(fullerene.natoms)
    # dis_vec = fullerene.get_all_distances(vector=True)
    # dis_vec /= (distances + 0.00001)[:, :, None]
    # orbital_p_vec = (distances[:, :, None] * dis_vec).sum(-2)
    # orbital_p_vec /= -np.linalg.norm(orbital_p_vec, 2, 1)[:, None]

    orbital_p_vec = np.zeros([fullerene.natoms,3])
    for i in range(fullerene.natoms):
        O = sphere_center_of_four_points(fullerene.positions[np.where(fullerene.atomADJ[i]==1)][0],
                                         fullerene.positions[np.where(fullerene.atomADJ[i]==1)][1],
                                         fullerene.positions[np.where(fullerene.atomADJ[i]==1)][2],
                                         fullerene.positions[i])
        orbital_p_vec[i]=fullerene.positions[i]-O
    orbital_p_vec /= -np.linalg.norm(orbital_p_vec, 2, 1)[:, None]
    if distance_cutoff:
        dis_mask_idx = np.where(distances>distance_cutoff)
        distances[dis_mask_idx]=0
        mask[dis_mask_idx]=0
    orbital_p_cos = (orbital_p_vec[None, :] * orbital_p_vec[:, None]).sum(-1) / 2 + 0.5

    t = para

    extend_adj = orbital_p_cos * 1 / (distances + 0.00001) ** 4

    sum_chi = np.linalg.eigh(t * extend_adj * mask)

    adj = fullerene.get_fullerenecage().circleADJ
    Napp = (adj * (adj.sum(-1) == 5)[None, :] * (adj.sum(-1) == 5)[:, None]).sum() / 2
    # sum_chi = sum_chi[:fullerene.natoms // 2 - int(fullerene.info["charge"])//2]

    return sum_chi[0], sum_chi[1], Napp


def store_csi(atomfile, circlefile, xyz_dir, target_path, para, _func=calculate_ext_csi, charge=0, all_xyz=False):
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
    para:
        see `calculate_ext_csi`
    _func:
        function to return the calculation of  `csi_val`, `csi_vectors`, `napp_val`
    charge: int
        the charge number of cages
    all_xyz:
        read and calculate all xyz coordinations from xyz_dir's files
    See Also
    --------
    data.spiral.adj_store, calculate_csi

    """
    spiral_num_list = []
    csi_list = []
    energy_list = []
    napp_list = []
    pa = re.compile("[0-9]+")
    pbar = tqdm(total=len(os.listdir(xyz_dir)))
    adjgener = adj_gener(atomfile, circlefile)
    for xyz_path in recursion_files(rootpath=xyz_dir, ignore_mode=True, format="xyz"):
        adj = next(adjgener)
        pbar.set_description(f'{xyz_path}')
        pbar.update()
        for f in list(simple_read_xyz_xtb(xyz_path))[-1] if not all_xyz else list(simple_read_xyz_xtb(xyz_path)):
            spiral_num = int(pa.findall(os.path.splitext(xyz_path)[0])[-1])
            assert spiral_num == adj["spiral_num"]
            atomadj = adj["atomadj"]
            circleadj = adj["circleadj"]
            energy = f.info["energy"]
            f.info["charge"] = charge
            fuller = FullereneFamily(spiral=spiral_num, atomADJ=atomadj, circleADJ=circleadj, atoms=f)
            spiral_num_list.append(spiral_num)
            csi_val, _, napp_val = _func(fuller, para=para)
            csi_list.append(csi_val)
            napp_list.append(napp_val)
            energy_list.append(energy)
    np.savez(target_path, csi_list=csi_list, spiral_num=np.array(spiral_num_list), energy=np.array(energy_list), napp=napp_list)


def _store_csi(args):
    logger.debug(f"_store_csi:{args}")
    atomfile, circlefile, xyz_dir, target_path, para, _func, charge, include_traj = args
    store_csi(atomfile, circlefile, xyz_dir, target_path, para, _func=_func, charge=charge, all_xyz=include_traj)


def mp_store_csi(atomdir, circledir, xyz_root_dir, target_dir, para=7, charge=0, recalculate=True, npz_file_suffix="xCSI", number_mask=None, _func=calculate_ext_csi, include_traj=False):
    """
    Batch process of calculating extended-CSI

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
        number = pa.findall(os.path.splitext(atomfile)[0])[-1]

        if number_mask is not None:
            if int(number) not in number_mask:
                continue

        basename = "C" + number
        xyz_dir = os.path.join(xyz_root_dir, basename)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        try:
            target_path = os.path.join(target_dir, basename + f"_{npz_file_suffix}.npz")
            args = atomfile, circlefile, xyz_dir, target_path, para, _func, charge, include_traj
            if not recalculate:
                if pathlib.Path(target_path).exists():
                    continue
            po.apply_async(func=_store_csi, args=(args,), error_callback=print_error)
        except FileNotFoundError:
            continue
    po.close()
    po.join()


if __name__ == '__main__':
    freeze_support()
    tqdm.set_lock(RLock())
    po = Pool(1, initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
    for num in [40, 50, 60, 70]:
        skip = False  # Use current file
        atomfile = r"C:\Work\CODE\DATA\bin\ADJ" + str(num)
        circlefile = r"C:\Work\CODE\DATA\circleADJ\ADJ" + str(num)

        charge_suffix = "undefined"

        para = 7  # seem to relate with integration of C-C p_z-p_z orbitals.
        for charge in [0, -2, -4, -6, 2, 4, 6]:
            if charge == 0:
                charge_suffix = ""
            elif charge > 0:
                charge_suffix = "_p" + str(abs(charge))
            elif charge < 0:
                charge_suffix = "_n" + str(abs(charge))

            xyz_dir = r"C:\Work\CODE\DATA\fullerxTBcal\xTBcal" + charge_suffix + "\C" + str(num)


            def target_path(num):
                return r"C:\Work\CODE\DATA\xCSI7\C" + str(num) + charge_suffix + "_xCSI.npz"


            # set ratio of distance part
            if not skip:
                args = atomfile, circlefile, xyz_dir, target_path(num), para, charge
                _store_csi(args)
    # csi = []
    # en = []

    # for num in (40, 50, 60, 70, 80):
    #     data = np.load(target_path(num))
    #     csi.extend(-data["csi_list"][:, :num // 2].sum(-1))
    #     en.extend(data["energy"] * Hartree / eV)

    # import matplotlib.pyplot as plt
    #
    # fig = plt.figure(figsize=[10, 10])
    # ax = fig.add_subplot(111)

    # fullerxtb_pred=np.load(r"C:\Work\CODE\PythonPro\FullereneDataParser\examples\fullerxtbData\FullXTB_pred.npy")
    # fullerxtb_ref=np.load(r"C:\Work\CODE\PythonPro\FullereneDataParser\examples\fullerxtbData\FullXTB_ref.npy")
    # fullerxtb_diff=np.load(r"C:\Work\CODE\PythonPro\FullereneDataParser\examples\fullerxtbData\FullXTB_dif.npy")

    # ax=fig.add_subplot(111)
    # print(len(csi))
    # print(len(fullerxtb_pred))
    # ax.scatter(fullerxtb_ref,fullerxtb_pred-fullerxtb_ref,marker="x")
    # diff=fullerxtb_pred-fullerxtb_ref
    # fullerenextb_filtered=[]
    # error=[]
    # idx=0
    # for ref1 in tqdm(en):
    #     ref2=np.inf
    #     while not np.allclose(ref1,ref2,rtol=1.e-8,atol=1.e-4):
    #         ref2 = fullerxtb_ref[idx]
    #         idx += 1
    #     fullerenextb_filtered.append(diff[idx-1])
    #     error.append(ref1-ref2)
    # print(diff[idx-1],ref1*eV/Hartree,ref2*eV/Hartree,fullerxtb_ref[idx-1],fullerxtb_pred[idx-1])

    # ax.scatter(fullerxtb_ref,fullerxtb_pred-fullerxtb_ref,marker="x",color="red")
    # ax.scatter(en, csi, marker="x")
    # ax.scatter(fullerenextb_filtered, csi, marker="x")
    # ax.scatter(fullerenextb_filtered, error, marker="x")
    # plt.show()
