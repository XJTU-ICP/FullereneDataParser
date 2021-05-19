# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : _dual.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import networkx as nx
import numpy as np


def get_dual(G: nx.Graph, force=False) -> nx.Graph:
    """
    Get the dual graph of a graph.
    If `force`, it will skip planarity check.

    Parameters
    ----------
    G: nx.Graph
    force: bool

    Returns
    -------
    nx.Graph:
        Daul graph
    """
    if not force:
        assert nx.check_planarity(G)[0] == True, "Only a planarable graph has its dual."
    D = nx.convert_matrix.to_numpy_matrix(G)
    M = G.number_of_edges()
    N = G.number_of_nodes()
    A = np.zeros([M, 3])
    fullerenedatapraser.graph.dual(D, M, N, A)
    return A


if __name__ == '__main__':
    import ase.build.molecule
    from fullerenedatapraser.molecular.fullerene import FullereneFamily

    atoms = ase.build.molecule("C60")
    f = FullereneFamily(spiral=1812,
                        atoms=atoms)
    print(get_dual(f.graph))
