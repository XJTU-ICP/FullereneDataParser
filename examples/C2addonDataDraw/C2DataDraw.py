# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : C2DataDraw.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np

import matplotlib.pyplot as plt

pred = np.load(r"predc2add.npy")
ref = np.load(r"refc2add.npy")

plt.scatter(pred,ref,marker="x")
plt.xlabel("pred")
plt.ylabel("ref")
plt.show()

