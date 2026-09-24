# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : atoms_test.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import os

from fullerenedataparser.io.xyz import simple_read_xyz_xtb

xyz_path = r"D:\CODE\#DATASETS\FullDB\xTBcal\C20\C20_000000001opt.xyz"

for f in list(simple_read_xyz_xtb(xyz_path)):
    energy = f.info["energy"]
    print(energy)
