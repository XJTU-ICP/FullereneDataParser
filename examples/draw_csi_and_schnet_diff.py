# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : draw_csi_and_schnet_diff.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from matplotlib import pyplot as plt
import numpy as np
from fullerenedataparser.io.recursion import recursion_files

# ['csi_list', 'spiral_num', 'energy', 'napp']
csifiles = recursion_files(r"D:\CODE\#DATASETS\FullDB\CSI", format="npz")
csilist = []
en_list=[]

for num, file in enumerate(csifiles):
    file = np.load(file)
    csi_value = file["csi_list"]
    energy_value = file["energy"]
    atoms = csi_value.shape[-1]
    mask = np.array([[1 for _ in range(atoms // 2)], [0 for _ in range(atoms // 2)]], dtype=bool).reshape(-1)
    if atoms != 0:
        csilist.extend(item for item in np.array((csi_value * mask).sum(-1)))
        en_list.extend(item for item in energy_value)

en_list=np.array(en_list)
# print(en_list)
plt.scatter([_ for i, _ in enumerate(en_list)], csilist)
plt.show()
