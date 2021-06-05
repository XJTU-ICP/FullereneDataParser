# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : xyz.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from ase.atoms import Atoms
from fullerenedatapraser.io import FileCommentError
from fullerenedatapraser.util.logger import Logger

logger = Logger(__name__, console_on=True)


def simple_read_xyz_xtb(filepath, index=None, read_comment=True):
    """
    Read atoms from .xyz files.
    Parameters
    ----------
    filepath:str
    index:slice
    read_comment:bool
        If read_comment, Atoms returned will have `info` values `comments` from comment line in xyz files.

    Returns
    -------
        Generator of Atoms.
    """
    with open(filepath, "r") as file:
        lines = file.readlines()
        natoms = int(lines[0])
        nimages = len(lines) // (natoms + 2)
        if index is None:
            index = slice(0, nimages)
        for i in range(*index.indices(nimages)):
            symbols = []
            positions = []
            n = i * (natoms + 2) + 2
            if read_comment:
                try:
                    comments = dict(energy=float(lines[n - 1].split()[1]))
                except IndexError:
                    if not len(lines[n - 1].split()):  # if there is no comment
                        raise FileCommentError(f"Comments not recognizable: {lines[n - 1]}.\n Try to set `read_comment=False`.")
                    else:
                        comments = {}
                except ValueError:
                    raise FileCommentError(f"It seems your comment is not format as 'xx:dd'. Please check your file or set `read_comment=False` in `simple_read_xyz_xtb()`.")
            else:
                comments = {}
            for line in lines[n:n + natoms]:
                symbol, x, y, z = line.split()[:4]
                symbol = symbol.lower().capitalize()
                symbols.append(symbol)
                positions.append([float(x), float(y), float(z)])
            yield Atoms(symbols=symbols, positions=positions, info=comments)
