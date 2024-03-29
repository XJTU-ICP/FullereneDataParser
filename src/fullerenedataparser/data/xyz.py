# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : xyz.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import io
from pathlib import Path
from typing import Generator, Optional, Union

from ase import Atoms

from fullerenedataparser.util.logger import Logger

logger = Logger(__name__, console_on=True)


def simple_read_xyz_xtb(fileobj: Union[Path,str, io.TextIOWrapper],
                        index: Optional[slice] = None,
                        read_comment: bool = True) -> Generator:
    """

    Parameters
    ----------
    fileobj:PathLike[str]
        .xyz format file
    index: None or slice
        If None, read all coordinations in .xyz file.
    read_comment: bool
        If read_comment, read the every second line of molecules.

    Returns
    -------
    Atoms:
        With info attribution from comment of .xyz file.
    """
    if isinstance(fileobj, Path) or isinstance(fileobj,str):
        fileobj = open(fileobj, "r")
    lines = fileobj.readlines()
    natoms = int(lines[0])
    nimages = len(lines) // (natoms + 2)  # Calculate the number of molecules.
    if index is None:
        index = slice(0, nimages)
    for i in range(*index.indices(nimages)):
        symbols = []
        positions = []
        n = i * (natoms + 2) + 2
        comments = {}
        if read_comment:
            try:
                comments = dict(energy=float(lines[n - 1].split()[1]))
            except IndexError:
                if not len(lines[n - 1].split()):
                    raise Exception(
                        f"Comments not recognizable: {lines[n - 1]}.\n Try to set `read_comment=False`.")
        for line in lines[n:n + natoms]:
            symbol, x, y, z = line.split()[:4]
            symbol = symbol.lower().capitalize()
            symbols.append(symbol)
            positions.append([float(x), float(y), float(z)])
        atom = Atoms(symbols=symbols, positions=positions, info=comments)
        logger.debug(
            f"Read {fileobj.name} done {i}/{natoms}. It is {atom.__str__()}.")
        yield atom
