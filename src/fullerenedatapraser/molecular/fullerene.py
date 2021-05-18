# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : fullerene.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from ase import Atoms
from fullerenedatapraser.util.functools import lazy_property
from fullerenedatapraser.util.logger import Logger

logger = Logger(__name__, console_on=True)


class FullereneFamily(Atoms):
    def __init__(self, spiral, nospiralflag=False, atomADJ=None, circleADJ=None, **kwargs):
        self.spiral = self.get_spiral(spiral, nospiralflag)
        self.atomADJ = atomADJ
        self.circleADJ = circleADJ
        if "atoms" in kwargs:
            super(FullereneFamily, self).__init__(symbols=kwargs["atoms"].symbols,
                                                  positions=kwargs["atoms"].positions,
                                                  info=kwargs["atoms"].info)
        self.natoms = len(self.positions)

    def get_spiral(self, spiral, nospiralflag=False):
        # test spiral
        assert isinstance(nospiralflag, bool)
        if not nospiralflag:
            if spiral is not None:
                assert isinstance(spiral, int)
            else:
                raise ValueError("No Sprial got."
                                 "If the fullerene doesn't have spiral number, please set `nospiralflag=True`")
        elif nospiralflag:
            if spiral:
                logger.warning("`nospiralflag` has been set to True."
                               f"Please notice the spiral {spiral} will be ignored.")
        return spiral

    @lazy_property
    def IPR(self):
        raise NotImplementedError

    @lazy_property
    def calculated_atomADJ(self):
        raise NotImplementedError

    @lazy_property
    def calculated_circleADJ(self):
        raise NotImplementedError
