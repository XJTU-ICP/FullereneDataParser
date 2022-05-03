# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : C60_59e.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from fullerenedatapraser.graph.visualize.cage import planarity_graph_draw
import matplotlib.colors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from ase.build import molecule

from fullerenedatapraser.molecular.fullerene import FullereneCage

C60 = molecule("C60")
f = FullereneCage(atoms=C60, spiral=1812)
# view(f)
ADJ = f.atomADJ
w, v = np.linalg.eigh(ADJ)
# [print(60-i,-w[i])for i in range(60)]
# C59 \pi
ADJ59 = np.delete(ADJ, 0, 0)
ADJ59 = np.delete(ADJ59, 0, 1)
w59, v59 = np.linalg.eigh(ADJ59)
# [print(59-i,-w59[i])for i in range(59)]


ax, graph_pos = planarity_graph_draw(f, sphere_ratio=0.9, parr_ratio=0.1, projection_point=16)
dis = v59 ** 2
dis_value = np.zeros([60, ])
dis_value[1:] = (dis[:, 29] - min(dis[:, 29])) / (max(dis[:, 29]) - min(dis[:, 29]))
print(dis_value)
cmap = matplotlib.pyplot.get_cmap("GnBu")

for idx, point in enumerate(dis_value):
    ax.add_patch(mpatches.Circle((float(graph_pos[idx, 0]), float(graph_pos[idx, 1])), radius=0.2, color=cmap(point) if idx != 0 else "Purple"))

plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=min(dis[:, 29]), vmax=max(dis[:, 29])), cmap=cmap), orientation="horizontal")
plt.margins(0, 0)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.show()

# ADJ58_56 = np.delete(ADJ59, 0, 0)
# ADJ58_56 = np.delete(ADJ58_56, 0, 1)
#
# ADJ58_55 = np.delete(ADJ59, 1, 0)
# ADJ58_55 = np.delete(ADJ58_55, 1, 1)
#
# w58_55, v58_55 = np.linalg.eigh(ADJ58_55)
# w58_56, v58_56 = np.linalg.eigh(ADJ58_56)
# [print(58 - i, -w58_56[i],-w58_55[i]) for i in range(58)]
