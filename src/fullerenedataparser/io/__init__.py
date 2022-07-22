# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : __init__.py.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

class MolecularIOError(Exception):
    """
    Base class for exception in molecular io.
    """


class FileNotMatchError(FileNotFoundError, MolecularIOError):
    """
    Exception for file not found or match.
    """


class FileContentError(Exception):
    """
    Base class for exception in file content illegal.
    """


class FileCommentError(FileContentError):
    """
    Exception for Comments in file is illegal.
    """
