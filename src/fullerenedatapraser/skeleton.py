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
import tempfile
from multiprocessing import cpu_count, Pool

from fullerenedatapraser import __version__
from fullerenedatapraser.data.spiral import adj_gener, adj_store
from fullerenedatapraser.io.recursion import recursion_files
from fullerenedatapraser.util.logger import Logger
from tqdm import tqdm

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"

logger = Logger(__name__, console_on=True)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from fullerenedatapraser.skeleton import fib`,
# when using this Python module as a library.

def store_spiral_output(atomfile, circlefile, targetfile):
    with tempfile.NamedTemporaryFile(prefix=f"{os.path.basename(atomfile)}_", dir=os.path.dirname(targetfile)) as f:
        logger.debug(f"{atomfile},{circlefile},{targetfile}")
        gener = adj_gener(atomfile, circlefile)
        adj_store(targetfile, gener)


def print_error(value):
    logger.error(f"Wrong when using process pool: {value}")


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

def read_spiral_output(atomdir=None, circledir=None, storedir="output"):
    logger.debug(f"Starting processing spiral output files. Using atomdir={atomdir} circledir={circledir} storedir={storedir}")
    if not (atomdir and circledir):
        raise ValueError("Either `atomdir` or `circledir` must be given.")
    if atomdir is None:
        raise NotImplementedError("Without `atomdir` I don't know what I could do.")
    elif circledir is None:
        raise NotImplementedError("Without `circle` I don't know what I could do.")
    else:
        logger.debug(f"Create process Pool. cpu_count={cpu_count()}")
        po = Pool(4)
        for atomfile in recursion_files(atomdir, format=""):
            pbar = tqdm(total=41)
            pbar.set_description(' Flow ')
            update = lambda *args: pbar.update()
            basename = os.path.basename(atomfile)
            circlefile = os.path.join(circledir, basename)
            targetfile = os.path.join(storedir, basename + ".h5")
            args = [atomfile, circlefile, targetfile]
            po.apply_async(func=_store_spiral_output, args=(args,), error_callback=print_error, callback=update)
        po.close()
        po.join()


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.

def _read_spiral_output(args):
    args.atomdir = os.path.abspath(args.atomdir)
    args.circledir = os.path.abspath(args.circledir)
    args.storedir = os.path.abspath(args.storedir)
    read_spiral_output(args.atomdir, args.circledir, args.storedir)


def _store_spiral_output(args):
    logger.debug("args")
    atomfile, circlefile, targetfile = args
    store_spiral_output(atomfile, circlefile, targetfile)


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

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formated message.

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

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m fullerenedatapraser.skeleton 42
    #
    run()
