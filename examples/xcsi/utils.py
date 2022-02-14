# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : utils.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import numpy as np


def charge_name_parse(charge_number: int):
    if isinstance(charge_number, int):
        if charge_number == 0:
            return ""
        elif charge_number > 0:
            return f"_p{charge_number}"
        elif charge_number < 0:
            return f"_n{-charge_number}"
    else:
        raise TypeError(f"`charge_number`: excepted `int` type, got {type(charge_number)} instead.")


def charges_draw_parse(charge_number: int):
    if isinstance(charge_number, int):
        if charge_number == 0:
            return [0, 0]
        elif charge_number > 0:
            return [1, charge_number // 2 - 1]
        elif charge_number < 0:
            return [2, -charge_number // 2 - 1]
    else:
        raise TypeError(f"`charge_number`: excepted `int` type, got {type(charge_number)} instead.")


def calculate_origin_csi(eval, napp, charged):
    """
    `CSI` by Wang et al.
    References
    ----------
    [Wang2018]  J. Chem. Theory Comput. 14, 1791–1810 (2018).
                Wang, Y., Díaz-Tendero, S., Alcamí, M. & Martín, F.
                Topology-Based Approach to Predict Relative Stabilities of Charged and Functionalized Fullerenes.

    Parameters
    ----------
    eval:numpy.array()
        eigen values of cage adjacent graph.

    napp: int
        Number of adjacent pentagon pairs. (Each pentagon-pentagon shared edge counts.)

    charge: int
        Charge.

    Returns
    -------
    `CSI` of input eigen values and napp.

    """
    atomnum = eval.shape[-1]
    evalsum = 0
    if charged > 0:
        evalsum = -eval[:, atomnum // 2 + 1:atomnum // 2 + 1 + charged // 2].sum(-1)
    elif charged < 0:
        evalsum = -eval[:, atomnum // 2 + charged // 2:atomnum // 2].sum(-1)
    elif charged == 0:
        evalsum = 0
    return evalsum + 0.2 * napp


def calculate_origin_csi_without_napp(eval, napp, charged):
    """
    `CSI` by Wang et al. But not add napp term.
    References
    ----------
    [Wang2018]  J. Chem. Theory Comput. 14, 1791–1810 (2018).
                Wang, Y., Díaz-Tendero, S., Alcamí, M. & Martín, F.
                Topology-Based Approach to Predict Relative Stabilities of Charged and Functionalized Fullerenes.

    Parameters
    ----------
    eval:numpy.array()
        eigen values of cage adjacent graph.

    napp: int
        Number of adjacent pentagon pairs. (Each pentagon-pentagon shared edge counts.)

    charge: int
        Charge.

    Returns
    -------
    `CSI` of input eigen values and napp.

    """
    atomnum = eval.shape[-1]
    evalsum = 0
    if charged > 0:
        evalsum = -eval[:, atomnum // 2 + 1:atomnum // 2 + 1 + charged // 2].sum(-1)
    elif charged < 0:
        evalsum = -eval[:, atomnum // 2 + charged // 2:atomnum // 2].sum(-1)
    elif charged == 0:
        evalsum = 0
    return evalsum + 0 * napp


def calculate_origin_csi_only_napp(eval, napp, charged):
    """
    `CSI` by Wang et al. But not add napp term.
    References
    ----------
    [Wang2018]  J. Chem. Theory Comput. 14, 1791–1810 (2018).
                Wang, Y., Díaz-Tendero, S., Alcamí, M. & Martín, F.
                Topology-Based Approach to Predict Relative Stabilities of Charged and Functionalized Fullerenes.

    Parameters
    ----------
    eval:numpy.array()
        eigen values of cage adjacent graph.

    napp: int
        Number of adjacent pentagon pairs. (Each pentagon-pentagon shared edge counts.)

    charge: int
        Charge.

    Returns
    -------
    `CSI` of input eigen values and napp.

    """
    return 0.2 * napp


def calculate_xcsi(eval, napp=None, charged=0):
    atomnum = eval.shape[-1]
    evalsum = eval[:, :atomnum // 2 + charged // 2-1].sum(-1)
    if napp is None:
        return evalsum
    else:
        return evalsum+0.2*napp
