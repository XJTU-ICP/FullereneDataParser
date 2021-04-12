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

import argparse
import logging
import os
import sys

from fullerenedatapraser import __version__
from fullerenedatapraser.calculator.csi import mp_store_csi
from fullerenedatapraser.data.spiral import read_spiral_output
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

def _read_spiral_output(args):
    args.atomdir = os.path.abspath(args.atomdir)
    args.circledir = os.path.abspath(args.circledir)
    args.storedir = os.path.abspath(args.storedir)
    read_spiral_output(args.atomdir, args.circledir, args.storedir)


def _process_stable_index(args):
    if args.stableindextype == "CSI":
        args.adjdir = os.path.abspath(args.adjdir)
        args.xyzdir = os.path.abspath(args.xyzdir)
        args.storedir = os.path.abspath(args.storedir)
        mp_store_csi(args.adjdir, args.xyzdir, args.storedir)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(prog="FDP",
                                     description="Praser toolsets for fullerene data.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"FullereneDataPraser {__version__}",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.INFO
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    subparsers = parser.add_subparsers(  # title="sub-command",
        metavar="subcommand",
        help="",
        required=True)
    # subcommand spiral
    subsubparser_spiral = subparsers.add_parser("spiral", help='Toolsets for deal with spiral algorithm and output files.')

    subsubparser_io = subparsers.add_parser("spiralIO", help='IO for deal with spiral algorithm and output files.')
    subsubparser_io.set_defaults(func=_read_spiral_output)
    subsubparser_io.add_argument(
        "--atom",
        help="Directory of atom adjacent matrix.",
        dest="atomdir",
        type=str,
        required=True
    )
    subsubparser_io.add_argument(
        "--circle",
        help="Directory of circle adjacent matrix.",
        dest="circledir",
        type=str,
        required=True
    )
    subsubparser_io.add_argument(
        "-o",
        "--storeDir",
        help="Directory of store spiral data.",
        dest="storedir",
        type=str,
        required=True
    )
    subsubparser_index = subparsers.add_parser("stableindex", help='Toolsets of some stable index.')
    subsubparser_index.set_defaults(func=_process_stable_index)
    subsubparser_index.add_argument(
        "--type",
        help="Index type",
        dest="stableindextype",
        choices=["CSI", ],
        type=str,
        required=True
    )
    subsubparser_index.add_argument(
        "--adj",
        help="Directory of adjacent files.",
        dest="adjdir",
        type=str,
        required=True
    )
    subsubparser_index.add_argument(
        "--xyz",
        help="Root directory of xyz directories.",
        dest="xyzdir",
        type=str,
        required=True
    )
    subsubparser_index.add_argument(
        "-o",
        "--storeDir",
        help="Directory of store index data.",
        dest="storedir",
        type=str,
        required=True
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    from fullerenedatapraser.util.config import setGlobValue
    setGlobValue("log_level", loglevel)
    logger.setLevel(loglevel)


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    logger = setup_logging(args.loglevel)
    args.func(args)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    run()
