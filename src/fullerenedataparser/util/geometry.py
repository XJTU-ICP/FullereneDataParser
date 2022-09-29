# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : geometry.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np


def sphere_center_of_four_points(point_a: np.ndarray, point_b: np.ndarray,
                                 point_c: np.ndarray,
                                 point_d: np.ndarray) -> np.ndarray:
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
    B = (pos_list * center_matrix).sum(axis=-1) + (
        (dis_matrix ** 2).sum(axis=-1)) / 2
    O = np.linalg.inv(center_matrix[:3]) @ B[:3]
    return O


def poav_of_four_points(point_a: np.ndarray,
                        point_b: np.ndarray,
                        point_c: np.ndarray,
                        point_pi: np.ndarray) -> np.ndarray:
    pos_list = np.array([point_a, point_b, point_c, point_pi])
    pos_tensor = pos_list[:3] - pos_list[-1]
    unit_matrix = pos_tensor / np.linalg.norm(pos_tensor, axis=-1)[:, None]
    cos_matrix = (unit_matrix[None, :] * unit_matrix[:, None]).sum(
        -1) / 2 + 0.5
    vec1 = pos_tensor[2] * cos_matrix[0][1] - pos_tensor[1] * cos_matrix[2][0]
    vec2 = pos_tensor[0] * cos_matrix[1][2] - pos_tensor[2] * cos_matrix[0][1]
    pi_vec = np.cross(vec2, vec1)
    # make sure pi_vec point to outside
    if np.inner(pos_tensor[:3].sum(0), pi_vec) > 0:
        pi_vec = -pi_vec
    return pi_vec / np.linalg.norm(pi_vec)


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button

    a = np.array([3.0908709, -1.1585005, 1.201424])
    e = np.array([3.1879245, -1.4574599, -0.1997005])
    c = np.array([3.2984981, -0.4301142, -1.1204138])
    b = np.array([2.3360057, -2.5814499, -0.476105])
    bond = np.linalg.norm(a - e)
    vecAE = a - e
    vecBE = b - e
    vecCE = c - e
    vecAE /= np.linalg.norm(vecAE)
    vecBE /= np.linalg.norm(vecBE)
    vecCE /= np.linalg.norm(vecCE)
    sqrt3 = np.sqrt(3) / 3
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ABC, = ax.plot(*np.array([a, b, c]).transpose(), marker="o")
    D = ax.scatter(*e, c='b')
    POAV, = ax.plot(*(poav_of_four_points(a, b, c, e) + e), marker="o")
    sphere_c = sphere_center_of_four_points(a, b, c, e)
    sphere_vec = e - sphere_c
    sphere_vec /= np.linalg.norm(sphere_vec)
    simple_sphere, = ax.plot(*(sphere_vec + e), marker="o")
    # ax.axis([0, 1, -10, 10])

    axcolor = 'lightgoldenrodyellow'

    bondA = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    bondB = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    bondC = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)

    sbondA = Slider(bondA, 'bondA', 1.3, 2, valinit=bond)
    sbondB = Slider(bondB, 'bondB', 1.3, 2, valinit=bond)
    sbondC = Slider(bondC, 'bondC', 1.3, 2, valinit=bond)


    def update(val):
        bA = sbondA.val
        bB = sbondB.val
        bC = sbondC.val
        newA = [vecAE[0] * bA, vecAE[1] * bA, vecAE[2] * bA] + e
        newB = [vecBE[0] * bB, vecBE[1] * bB, vecBE[2] * bB] + e
        newC = [vecCE[0] * bC, vecCE[1] * bC, vecCE[2] * bC] + e
        print(newA, newB, newC)
        ABC.set_data_3d(*np.array([newA, newB, newC]).transpose())
        POAV.set_data_3d(*
                         (poav_of_four_points(np.array(newA),
                                              np.array(newB),
                                              np.array(newC),
                                              e) + e))
        sphere_c = sphere_center_of_four_points(np.array(newA),
                                                np.array(newB),
                                                np.array(newC), e)
        sphere_vec = e - sphere_c
        sphere_vec /= np.linalg.norm(sphere_vec)
        sphere_vec += e
        simple_sphere.set_data_3d(*sphere_vec)
        fig.canvas.draw_idle()


    sbondA.on_changed(update)
    sbondB.on_changed(update)
    sbondC.on_changed(update)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


    def reset(event):
        sbondA.reset()
        sbondB.reset()
        sbondC.reset()


    button.on_clicked(reset)

    # rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
    # radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)

    plt.show()
