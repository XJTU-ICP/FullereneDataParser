# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : C2DataTest.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import dpdata
import pathlib
import ase
import numpy as np
from ase.visualize import view

"""
convert dpdata to lightmolnet db.
"""

c2addon = r"D:\CODE\#DATASETS\dpdata_c2addon"

ms = dpdata.MultiSystems()
for dir in pathlib.Path(c2addon).iterdir():
    ms.append(dpdata.LabeledSystem(dir.as_posix(), fmt="deepmd/npy"))

for ls in ms:
    ls: dpdata.LabeledSystem
    for item in ls:
        data = item.data
        symbols = [data["atom_names"][data["atom_types"][i]] for i in range(data["atom_numbs"][-1])]
        atoms = ase.Atoms(symbols=symbols,
                          positions=data["coords"][-1] if len(data["coords"]) == 1 else None)

