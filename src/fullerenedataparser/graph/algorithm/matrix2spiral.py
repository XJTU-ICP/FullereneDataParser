# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : matrix2spiral.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from ase.io.gaussian import read_gaussian_in
from tqdm import tqdm

from fullerenedataparser.molecular.fullerene import FullereneCage
from src.fullerenedataparser.io.xyz import simple_read_xyz_xtb


# slow method
def matrix2spiral_slow(input_path, circle_num, eigh_ref):
    """
    Search spiral of an offering .gjf file from circle adj database.
    Print on screen.

    Parameters
    ----------
    input_path: xyz or gjf file path string.
    circle_num: !!! the number of circle
    eigh_ref: list
        list store the eigh values by np.linalg.eigh()

    Returns
    -------

    """
    input_path = pathlib.Path(input_path)
    if input_path.suffix == ".gjf":
        g_in = read_gaussian_in(open(input_path, "r"))
    elif input_path.suffix == ".xyz":
        atomlist = list(simple_read_xyz_xtb(input_path.as_posix(), read_comment=False))
        if len(atomlist) == 1:
            g_in = atomlist[0]
        else:
            raise ValueError(
                f"There are more than one atoms in file {input_path.name}. Please check.")
    else:
        raise ValueError(f"Unrecognizable extension name {input_path.suffix}.")
    cage = FullereneCage(spiral=-1, atoms=g_in)
    assert g_in.get_global_number_of_atoms() == (circle_num - 2) * 2
    circle_adj = np.zeros([circle_num, circle_num])
    circle_edge = np.array(cage.circle_finder.get_dual_edge_list())
    circle_adj[circle_edge[:, 0], circle_edge[:, 1]] = 1
    circle_adj[circle_edge[:, 1], circle_edge[:, 0]] = 1
    w, v = np.linalg.eigh(circle_adj)
    for idx, item in tqdm(enumerate(eigh_ref, 1)):
        if np.allclose(item, w):
            print(f"Seem like spiral = {idx} for file {pathlib.Path(input_path).name}.")


if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf, linewidth=500)
    ADJ_DB_FILE = r"D:\CODE\#DATASETS\FullDB\circleadj\ADJ86"
    atom_num = 86
    circle_num = atom_num * 1 // 2 + 2
    REF = []
    eigh_ref = []
    # with open(ADJ_DB_FILE, "r") as f:
    #     fline = f.readline()  # generator line
    #     tbar = tqdm(desc="Read DB")
    #     while fline:
    #         flag = 0
    #         lines = []
    #         fline = f.readline()  # spiral number line
    #         for i in range(circle_num):
    #             line = np.fromstring(f.readline(), dtype=int, sep=" ")
    #             if line.shape[0]!=0:
    #                 lines.append(line)
    #         if lines:
    #             adj = np.array(lines)
    #             REF.append(adj)
    #             w, _ = np.linalg.eigh(adj)
    #             eigh_ref.append(w)
    #             tbar.update(1)
    # matrix2spiral_slow(r"D:\Documents\WeChat Files\hanyanbo231270\FileStorage\File\2022-03\C86-15.gjf", circle_num, eigh_ref)
    # matrix2spiral_slow(r"D:\Documents\WeChat Files\hanyanbo231270\FileStorage\File\2022-03\C86-11.gjf", circle_num, eigh_ref)
    g_in = read_gaussian_in(open(r"D:\Documents\WeChat Files\hanyanbo231270\FileStorage\File\2022-03\C86-15.gjf", "r"))
    cage1 = FullereneCage(spiral=-1, atoms=g_in)
    cage1.draw(sphere_ratio=0.5, parr_ratio=0.2)

    g_in = read_gaussian_in(open(r"D:\Documents\WeChat Files\hanyanbo231270\FileStorage\File\2022-03\C86-11.gjf", "r"))
    cage2 = FullereneCage(spiral=-1, atoms=g_in)
    cage2.draw(sphere_ratio=0.5, parr_ratio=0.2)
    plt.show()
