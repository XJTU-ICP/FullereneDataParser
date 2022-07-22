# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : geometry.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np


def sphere_center_of_four_points(point_a: np.ndarray, point_b: np.ndarray, point_c: np.ndarray, point_d: np.ndarray) -> np.ndarray:
    """
    Calculate the center of sphere for four non-coplanar points

    Parameters
    ----------
    point_a: np.ndarray
        point coordinate
    point_b: np.ndarray
        point coordinate
    point_c: np.ndarray
        point coordinate
    point_d: np.ndarray
        point coordinate

    Returns
    -------
    np.ndarray
        coordinate of sphere center

    Notes
    -----
    This function based on these equations:

    .. math:: \mathbf{OD}*2(\mathbf{DA}+\mathbf{DB}+\mathbf{DC})=-(|DA|^2+|DB|^2+|DC|^2)


    Same for point :math:`A,B,C`, which leads us to a matrix form

    .. math:: \mathbf{Or'}\mathbf{O}^T=[A*O'_A+|AD|^2+|AB|^2+|AC|^2,B*O'_B+|BA|^2+|BC|^2+|BD|^2,C*O'_C+|CA|^2+|CB|^2+|CD|^2]^T

    where :math:`O` is the centor of the sphere, :math:`\mathbf{O'}` is the matrix as below:

    .. math:: \mathbf{O'}=[\mathbf{AD+AB+AC},\mathbf{BA+BC+BD},\mathbf{CA+CB+CD}]^T
    """
    pos_list = np.array([point_a, point_b, point_c, point_d])
    pos_tensor = pos_list - pos_list[:, None, :]
    dis_matrix = np.linalg.norm(pos_tensor, axis=-1)
    center_matrix = pos_tensor.sum(axis=-2)
    B = (pos_list * center_matrix).sum(axis=-1) + ((dis_matrix ** 2).sum(axis=-1)) / 2
    O = np.linalg.inv(center_matrix[:3]) @ B[:3]
    return O
