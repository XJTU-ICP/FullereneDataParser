# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : codelab.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import os
from multiprocessing import Pool

from fullerenedatapraser.data.spiral import adj_gener
from fullerenedatapraser.util.logger import Logger

logger = Logger(__name__, console_on=True)


def work(atomfile, circlefile, targetfile):
    gener = adj_gener(atomfile, circlefile)
    adj_store(targetfile, gener)


if __name__ == '__main__':
    from fullerenedatapraser.data.spiral import adj_store
    from fullerenedatapraser.io.recursion import recursion_files
    from multiprocessing import cpu_count

    atomdir = r"C:\Work\CODE\DATA\bin"
    circledir = r"C:\Work\CODE\DATA\circleADJ"
    targetdir = r"C:\Work\CODE\DATA\test"
    po = Pool(cpu_count())
    for atomfile in recursion_files(atomdir, format=""):
        basename = os.path.basename(atomfile)
        circlefile = os.path.join(circledir, basename)
        targetfile = os.path.join(targetdir, basename + ".h5")
        po.apply_async(func=work, args=(atomfile, circlefile, targetfile))
    po.close()
    po.join()
