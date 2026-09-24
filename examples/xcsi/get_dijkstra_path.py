# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : get_dijkstra_path.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import pathlib

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from fullerenedataparser.io.xyz import simple_read_xyz_xtb
from fullerenedataparser.molecular.fullerene import FullereneCage

XYZ_STORE_PREFIX = r"D:\CODE\#DATASETS\FullDB\xTBcal"
N = 50
xsi_list = []
xsi_list_withoutangle=[]
en = []
for cage in list((pathlib.Path(XYZ_STORE_PREFIX) / f"C{N}").iterdir()):
    C60 = list(simple_read_xyz_xtb(cage.as_posix()))[0]
    fuller = FullereneCage(atoms=C60, spiral=-1)
    G = fuller.graph
    adj = fuller.atomADJ
    length = nx.all_pairs_shortest_path_length(G)

    length_mat = np.zeros([N, N])

    for item in length:
        for t, v in item[1].items():
            length_mat[item[0]][t] = v
    length_max = length_mat.max(-1)*2/3
    approx_dix = np.sqrt(length_max[:, None] @ length_max[None, :])
    dis_noangle = np.nan_to_num(1/length_mat**2) * (
                np.ones_like(length_mat) - np.eye(N))
    dis2 = adj
    xsi_list_withoutangle.append((np.linalg.eigh(dis_noangle)[0])[:N//2].sum())
    xsi_list.append((np.linalg.eigh(dis2)[0])[:N//2].sum())
    en.append(fuller.info["energy"])
plt.scatter(xsi_list-min(xsi_list), en)
plt.scatter(xsi_list_withoutangle-min(xsi_list_withoutangle), en)

print(np.corrcoef([xsi_list,xsi_list_withoutangle,en]))
plt.show()