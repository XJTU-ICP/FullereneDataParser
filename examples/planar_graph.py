# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : planar_graph.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import ase
from ase.neighborlist import NeighborList
from ase.neighborlist import build_neighbor_list, natural_cutoffs, get_connectivity_matrix
from ase.build import molecule
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

atoms = molecule("C60")
fig = plt.figure()
ax1 = plt.subplot(1, 1, 1, projection='3d')
pos = atoms.positions
posc=pos[pos[:,1]< -1.5]

func2=interpolate.interpn(pos[:,0],pos[:,1],pos[:,2])
length2 = np.linspace(-3,3,50)
width2 = np.linspace(-3,3,50)
current2=func2(width2,length2)
J,K = np.meshgrid(width2,length2)

WHP2=ax1.plot_surface(J,current2,K,alpha=.8,antialiased=True)
ax1.scatter(pos[:,0],pos[:,1],pos[:,2])
plt.show()