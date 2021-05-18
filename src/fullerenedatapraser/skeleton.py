"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = fullerenedatapraser.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import logging
import os
import sys

import click

try:
    import deprecation
except ModuleNotFoundError:
    class deprecation:
        @classmethod
        def deprecated(*args, **kwargs):
            logger.warning("Please install module `deprecation` by `conda install deprecation -c conda-forge.`")
            sys.exit(1)

from fullerenedatapraser.calculator.csi import mp_store_csi
from fullerenedatapraser.util.logger import Logger

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"

logger = Logger(__name__, console_on=True)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from fullerenedatapraser.skeleton import fib`,
# when using this Python module as a library.


# def fib(n):
#     """Fibonacci example function
#
#     Args:
#       n (int): integer
#
#     Returns:
#       int: n-th Fibonacci number
#     """
#     assert n > 0
#     a, b = 1, 1
#     for i in range(n - 1):
#         a, b = b, a + b
#     return a


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.

@click.group()
@click.version_option()
@click.option('-v', '--verbose', count=True)
def fullertool(verbose):
    """
    Praser toolsets for fullerene data.
    By MIT License.(2021-)\n
    Use `-v` and `-vv` to set log level.
    """
    from fullerenedatapraser.util.config import setGlobValue
    if 2 > verbose > 0:
        setGlobValue("log_level", logging.INFO)
        logger.setLevel(logging.INFO)
    if verbose > 1:
        setGlobValue("log_level", logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    del setGlobValue
    pass


@fullertool.command()
def spiral():
    """
    Toolsets for deal with spiral algorithm and output files. (TODO)
    """
    # TODO: Spiral binary.
    click.echo(click.style("`Spiral` integration is Unavailable now.", fg="red"), err=True)
    # raise NotImplementedError("`Spiral` integration is in Working.")


@fullertool.command()
@click.option("--type", "-t", "stableindextype", help="Index type of stability.", type=click.Choice(["CSI", ]))
@click.option("--atom", "--at", "atomdir", help="Directory of atom adjacent matrix.", prompt="Directory of atom adjacent matrix")
@click.option("--circle", "--ci", "circledir", help="Directory of circle adjacent matrix.", prompt="Directory of circle adjacent matrix")
@click.option("--xyzdir", "--xyz", "xyzdir", help="ROOT directory of xyz directories.", prompt="ROOT directory of xyz directories")
@click.option("--stor", "-o", "storedir", help="Directory to store index data.", prompt="Directory to store index data")
def stableindex(stableindextype, atomdir, circledir, xyzdir, storedir):
    """
    Toolsets of some stable index. \
    You will get `.npz` files in `storedir` directory.\n
    In `.npz` files, there will be there subdata named:\n
     'csi_list', 'spiral_num' and 'energy'.
    """
    if stableindextype == "CSI":
        atomdir = os.path.abspath(atomdir)
        circledir = os.path.abspath(circledir)
        xyzdir = os.path.abspath(xyzdir)
        storedir = os.path.abspath(storedir)
        mp_store_csi(atomdir, circledir, xyzdir, storedir)


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    fullertool()
