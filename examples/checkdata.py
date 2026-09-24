# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : checkdata.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import matplotlib.pyplot as plt
import numpy as np
from ase.visualize import view
from ase.atoms import Atoms
from fullerenedataparser.molecular.fullerene import FullereneFamily

# fig = plt.figure()
# ax=plt.axes(projection="3d")

import dpdata

ls = dpdata.MultiSystems().from_dir(r"D:\CODE\#DATASETS\dpdata_c2addon", "", "deepmd/npy", recursive=False, Labeled=False)
print(list(map(dpdata.System.get_nframes, ls)))


pos = ls["C50"].data["coords"][3]
atoms1 = Atoms(symbols=["C" for _ in range(50)],
                   positions=pos)
view([atoms1])
print(
    pos
)

