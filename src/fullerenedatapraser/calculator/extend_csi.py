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

import numpy as np
from fullerenedatapraser.data.spiral import adj_gener
from fullerenedatapraser.io.recursion import recursion_files
from fullerenedatapraser.io.xyz import simple_read_xyz_xtb
from fullerenedatapraser.molecular.fullerene import FullereneFamily
from fullerenedatapraser.util.logger import Logger
from fullerenedatapraser.util.mp import print_error
from tqdm import tqdm

from fullerenedatapraser.util.config import setGlobValue

setGlobValue("log_level", logging.DEBUG)
logger = Logger(__name__, console_on=True)


def calculate_ext_csi(fullerene: FullereneFamily, para=7):
    """
    Implemention of extended
    Parameters
    ----------
    fullerene:FullereneFamily
        molecule Instance of Fullerene.
    Returns
    -------
        CSI
    References
    ----------

    """

    assert fullerene.natoms % 2 == 0, f"Not A classical Fullerene. Check your input atoms: {fullerene}."
    # csi_adj = fullerene.atomADJ # not used actually

    distances=fullerene.get_all_distances()
    mask = np.ones_like(distances)-np.eye(fullerene.natoms)
    dis_vec=fullerene.get_all_distances(vector=True)
    dis_vec/=(distances+0.00001)[:,:,None]
    orbital_p_vec = (distances[:, :, None] * dis_vec).sum(-2)
    orbital_p_vec /= -np.linalg.norm(orbital_p_vec, 2, 1)[:, None]

    orbital_p_cos=(orbital_p_vec[None, :] * orbital_p_vec[ :, None]).sum(-1) / 2 + 0.5

    t=para

    extend_adj = orbital_p_cos*1/(distances+0.0001)**4


    sum_chi = np.linalg.eigh(t* extend_adj*mask)
    sum_chi=sum_chi[:fullerene.natoms // 2]

    return sum_chi[0],sum_chi[1]


def store_csi(atomfile, circlefile, xyz_dir, target_path,para, _func=calculate_ext_csi):
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
    for xyz_path in recursion_files(rootpath=xyz_dir, ignore_mode=True,format="xyz"):
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
        csi_list.append(_func(fuller,para=para)[0])
        energy_list.append(energy)
    np.savez(target_path, csi_list=csi_list, spiral_num=np.array(spiral_num_list), energy=np.array(energy_list))


def _store_csi(args):
    logger.debug(f"_store_csi:{args}")
    atomfile, circlefile, xyz_dir, target_path, para = args
    store_csi(atomfile, circlefile, xyz_dir, target_path, para)


def mp_store_csi(atomdir, circledir, xyz_root_dir, target_dir,para = 7, _suffix="xCSI"):
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
        basename = "C" + pa.findall(os.path.splitext(atomfile)[0])[-1]
        xyz_dir = os.path.join(xyz_root_dir, basename)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        try:
            target_path = os.path.join(target_dir, basename + f"_{_suffix}.npz")
            args = atomfile, circlefile, xyz_dir, target_path, para
            po.apply_async(func=_store_csi, args=(args,), error_callback=print_error)
        except FileNotFoundError:
            continue
    po.close()
    po.join()


if __name__ == '__main__':
    from ase.units import  Hartree,eV
    num=80
    skip=True # Use current file
    atomfile = r"C:\Work\CODE\DATA\bin\ADJ"+str(num)
    circlefile = r"C:\Work\CODE\DATA\circleADJ\ADJ"+str(num)
    xyz_dir = r"C:\Work\CODE\DATA\fullerxTBcal\xTBcal\C"+str(num)
    para=7
    def target_path(num):
        return r"C:\Work\CODE\DATA\xCSI7\C"+str(num)+"_xCSI.npz"
    # set ratio of distance part
    if not skip:
        args = atomfile, circlefile, xyz_dir, target_path(num), para
        _store_csi(args)
    csi=[]
    en=[]
    for num in (40,50,60,70,80):
        data=np.load(target_path(num))
        csi.extend(-data["csi_list"][:,:num//2].sum(-1))
        en.extend(data["energy"]*Hartree/eV)
    import matplotlib.pyplot as plt
    from tqdm import trange

    fig = plt.figure(figsize=[10,10])
    ax=fig.add_subplot(111)


    # fullerxtb_pred=np.load(r"C:\Work\CODE\PythonPro\FullereneDataPraser\examples\fullerxtbData\FullXTB_pred.npy")
    # fullerxtb_ref=np.load(r"C:\Work\CODE\PythonPro\FullereneDataPraser\examples\fullerxtbData\FullXTB_ref.npy")
    # fullerxtb_diff=np.load(r"C:\Work\CODE\PythonPro\FullereneDataPraser\examples\fullerxtbData\FullXTB_dif.npy")

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
    ax.scatter(en,csi,marker="x")
    # ax.scatter(fullerenextb_filtered, csi, marker="x")
    # ax.scatter(fullerenextb_filtered, error, marker="x")
    plt.show()
