# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : config.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import logging


class GlobalVar:
    log_level = logging.INFO # work for


def getGlobValue(name):
    return getattr(GlobalVar, name, None)


def setGlobValue(name, value):
    setattr(GlobalVar, name, value)

class SetModuleEnvValue:
    def __init__(self,name,value):
        self._GlobalVarName=name
        self._GlobalVarValue=getGlobValue(name)
        self._changeValue=value
    def __enter__(self):
        setGlobValue(self._GlobalVarName, self._changeValue)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._GlobalVarValue is None:
            delattr(GlobalVar,self._GlobalVarName)
        else:
            setGlobValue(self._GlobalVarName,self._GlobalVarValue)
