# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : fullerene.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import logging
from typing import Iterable

import networkx as nx
import numpy as np
from ase import Atoms
from ase.neighborlist import natural_cutoffs, NeighborList

from fullerenedataparser.util.functools import lazy_property
from fullerenedataparser.util.logger import Logger

logger = Logger(__name__, console_on=True)


class FullereneFamily(Atoms):
    def __init__(
        self,
        spiral,
        nospiralflag=False,
        atomADJ=None,
        circleADJ=None,
        **kwargs,
    ):
        """

        Parameters
        ----------
        spiral
        nospiralflag
        atomADJ
        circleADJ
        atoms:ase.atoms.Atoms
            `Atoms` object for details.
        """
        self.spiral = self._get_spiral(spiral, nospiralflag)
        self.nospiralflag = nospiralflag
        self._atomADJ = atomADJ
        self._circleADJ = circleADJ
        if "atoms" in kwargs:
            assert isinstance(kwargs["atoms"], Atoms), f"`atoms` must be an instance of `ase.atoms.Atoms`, got {type(kwargs['atoms'])}"
            super(FullereneFamily, self).__init__(symbols=kwargs["atoms"].symbols,
                                                  positions=kwargs["atoms"].positions,
                                                  info=kwargs["atoms"].info)
        self.natoms = len(self.positions)

    @property
    def atomADJ(self):
        if self._atomADJ is not None:
            return self._atomADJ
        else:
            return self.calculated_atomADJ

    @property
    def circleADJ(self):
        if self._circleADJ is not None:
            return self._circleADJ
        else:
            return self.calculated_circleADJ

    def _get_spiral(self, spiral, nospiralflag=False):
        # test spiral
        assert isinstance(nospiralflag, bool)
        if not nospiralflag:
            if spiral is not None:
                assert isinstance(spiral, int)
                return spiral
            else:
                raise ValueError("No Sprial got."
                                 "If the fullerene doesn't have spiral number, please set `nospiralflag=True`")
        elif nospiralflag:
            if spiral:
                logger.warning("`nospiralflag` has been set to True."
                               f"Please notice the spiral {spiral} will be ignored.")
            return None

    @lazy_property
    def IPR(self):
        raise NotImplementedError

    @lazy_property
    def calculated_atomADJ(self):
        cutoffs = natural_cutoffs(self)
        neighborList = NeighborList(cutoffs, self_interaction=False, bothways=True)
        neighborList.update(self)
        atomADJ = neighborList.get_connectivity_matrix(sparse=False)
        if (atomADJ.sum(-1) != 3).any():
            atomADJ = np.zeros_like(atomADJ)
            logging.warning(f"More than 3 neighbors by ase found for {self.spiral}."
                            f"Trying using first 3 shortest distance.")
            neighborDis: np.ndarray = self.get_all_distances()
            neighborSorted = np.argsort(neighborDis)
            atomADJ[np.arange(self.natoms)[:, None], neighborSorted[:, 1:4]] = 1
        return atomADJ

    @lazy_property
    def calculated_circleADJ(self):
        edge_list = self.circle_finder.get_dual_edge_list()
        circleADJ = np.zeros([self.circle_finder.face_size,self.circle_finder.face_size])
        for item in edge_list:
            circleADJ[item[0],item[1]]=1
            circleADJ[item[1], item[0]] = 1
        return circleADJ

    @lazy_property
    def graph(self) -> nx.Graph:
        return nx.from_numpy_array(self.atomADJ, create_using=nx.Graph)

    @lazy_property
    def circle_finder(self):
        raise NotImplementedError

    def get_fullerenecage(self):
        """
        `get_fullerenecage`: return a FullereneCage Instance.
        Returns
        -------
        FullereneCage:

        """
        # warnings.warn(f"This Function `get_fullerenecage` is still in progress")
        return FullereneCage(spiral=self.spiral, nospiralflag=self.nospiralflag, atoms=self, atomADJ=self.atomADJ, circleADJ=self.circleADJ)


class FullereneCage(FullereneFamily):
    """
    One Cage which is planarity in FullereneFamily.
    """

    def __init__(self, *args, **kwargs):
        super(FullereneCage, self).__init__(*args, **kwargs)

    def _check_planarity(self):
        raise NotImplementedError

    @lazy_property
    def circle_finder(self):
        from fullerenedataparser.graph.algorithm import dual
        return dual.py_graph_circle_finder(len(self.graph.edges), np.array(self.graph.edges).data)

    @lazy_property
    def circle_vertex_list(self) -> Iterable[np.ndarray]:
        return self.circle_finder.get_face_vertex_list()

    def draw(self, sphere_ratio=0.2, parr_ratio=0.8, path=None, atom_label=True, projection_circle_idx=0,ax=None):
        """

        Parameters
        ----------
        sphere_ratio: sphere projection part of the result.
        parr_ratio: parallel projection part of the result.
        path
        atom_label
        projection_circle_idx:int
            if projection_circle_idx>=0:
                project from hexagon,
            if projection_circle_idx<0：
                project from pentagon
        ax: matplotlib axes
            if None, use new axes.
        Returns
        -------

        """
        from fullerenedataparser.graph.visualize.cage import planarity_graph_draw
        ax, graph_pos = planarity_graph_draw(self, sphere_ratio=sphere_ratio, parr_ratio=parr_ratio, path=path, atom_label=atom_label, projection_point=projection_circle_idx,ax=ax)
        return ax, graph_pos


if __name__ == '__main__':
    import ase.build
    import networkx as nx

    # np.set_printoptions(threshold=np.inf)
    # np.set_printoptions(linewidth=500)

    atoms = ase.build.molecule("C60")
    f = FullereneFamily(spiral=1812, atoms=atoms)
    f = f.get_fullerenecage()
    # print(f.circle_vertex_list)
    # f.draw(sphere_ratio=0.8,parr_ratio=0.5,path=r"C:\Users\45990\Desktop\31876.png")
    f.draw(sphere_ratio=0.8, parr_ratio=0.4)
