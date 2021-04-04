# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : fullerene.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from ase import Atoms
from fullerenedatapraser.util.logger import Logger
from fullerenedatapraser.util.functools import lazy_property

logger = Logger(__name__, console_on=True)

class FullereneFamily(Atoms):
    def __init__(self,spiral,nospiralflag=False,**kwargs):
        self.spiral=self.get_spiral(spiral,nospiralflag)
        super(Fullerene, self).__init__(**kwargs)

    def get_spiral(self,spiral,nospiralflag):
        # test spiral
        assert isinstance(nospiralflag,bool)
        if not nospiralflag:
            if spiral is not None:
                assert isinstance(spiral,int)
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

