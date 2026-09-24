# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : testimport.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import pathlib
from examples.test import readG16Log

f = r"C:\Users\hanyanbo98\PycharmProjects\FullereneDataPraser\tests\files\logfiles"
filelist = pathlib.Path(f).iterdir()
for filename in filelist:
    if filename.as_posix().endswith(".log"):
        print(readG16Log(filename))
