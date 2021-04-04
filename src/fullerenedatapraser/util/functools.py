# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : functools.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import functools
import sys


def lazy_property(func):
    if sys.version_info >= (3, 8):
        return functools.cached_property()
    else:
        attr_name = "_lazy_" + func.__name__

        @property
        def _lazy_property(self):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, func(self))
            return getattr(self, attr_name)

        return _lazy_property
