# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : fullerene.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import warnings

import networkx as nx
from ase import Atoms
from ase.neighborlist import natural_cutoffs, NeighborList
from fullerenedatapraser.util.functools import lazy_property
from fullerenedatapraser.util.logger import Logger

logger = Logger(__name__, console_on=True)


class FullereneFamily(Atoms):
    def __init__(self, spiral, nospiralflag=False, atomADJ=None, circleADJ=None, **kwargs):
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
            return self.atomADJ
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
        return neighborList.get_connectivity_matrix(sparse=False)

    @lazy_property
    def calculated_circleADJ(self):
        raise NotImplementedError

    @lazy_property
    def graph(self):
        return nx.from_numpy_array(self.atomADJ, create_using=nx.Graph)

    @lazy_property
    def cycle_finder(self):
        raise NotImplementedError

    def get_fullerenecage(self):
        """
        `get_fullerenecage`: return a FullereneCage Instance.
        Returns
        -------
        FullereneCage:

        """
        warnings.warn(f"This Function `get_fullerene` is still in progress")
        return FullereneCage(spiral=self.spiral,nospiralflag=self.nospiralflag,atoms=self)


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
        from fullerenedatapraser.graph.algorithm import dual
        return dual.py_graph_circle_finder(len(self.graph.edges), np.array(self.graph.edges).data)

    @lazy_property
    def circle_vertex_list(self):
        return self.circle_finder.get_face_vertex_list()

    def draw(self,deformation_ratio=0.2, path=None):
        from fullerenedatapraser.graph.visualize.cage import planarity_graph_draw
        planarity_graph_draw(self,deformation_ratio=deformation_ratio, path=path)


if __name__ == '__main__':
    import ase.build
    import numpy as np
    from fullerenedatapraser.io.xyz import simple_read_xyz_xtb

    # np.set_printoptions(threshold=np.inf)
    # np.set_printoptions(linewidth=500)

    atoms = ase.build.molecule("C60")
    f = FullereneFamily(spiral=1812, atoms=atoms)
    f = f.get_fullerenecage()
    # print(f.circle_vertex_list)
    f.draw(deformation_ratio=0.3,path=None)
