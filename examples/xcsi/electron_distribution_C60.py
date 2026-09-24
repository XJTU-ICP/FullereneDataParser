# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : electron_distribution_C60.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

# 2022/04/24 test the fulleren C60 electron distribution

import sys

import ase
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from fullerenedataparser.molecular.fullerene import FullereneCage
from ase.build import molecule
from ase.visualize import view
from ase.io.xyz import write_xyz
import matplotlib.patches as mpatches

from fullerenedataparser.graph.visualize.cage import planarity_graph_draw

C60 = molecule("C60")
f = FullereneCage(atoms=C60, spiral=1812)

ax, graph_pos = planarity_graph_draw(f, sphere_ratio=0.9, parr_ratio=0.1, projection_point=16)

# view(f)
ADJ = f.atomADJ
w, v = np.linalg.eigh(ADJ)
# [print(60-i,-w[i])for i in range(60)]
# C59 \pi

dis = v**2
dis = (v**2)[:,-28:].sum(axis=-1)

dis_value= (dis[:] - min(dis[:])) / (max(dis[:]) - min(dis[:]))
print(dis)

cmap = matplotlib.pyplot.get_cmap("Blues")

for idx, point in enumerate(dis_value):
    ax.add_patch(mpatches.Circle((float(graph_pos[idx, 0]), float(graph_pos[idx, 1])), radius=0.2, color=cmap(point)))

plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=min(dis[:]), vmax=max(dis[:])), cmap=cmap), orientation="horizontal")
plt.margins(0, 0)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.show()
