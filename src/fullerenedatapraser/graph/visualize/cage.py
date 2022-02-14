# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : cage.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from fullerenedatapraser.molecular.fullerene import FullereneCage


def planarity_graph_draw(cage: FullereneCage,
                         sphere_ratio: float = 0.8,
                         parr_ratio: float = 0.2,
                         projection_point: int = 0,
                         path=None,
                         pentage_color="orange",
                         pentage_alpha=0.5,
                         antialiased=True,
                         line_color="orange",
                         line_alpha=0.5,
                         atom_label=True):
    """
    Draw fullerene planarity graph combinating parrallel and hemi-sphere projection.

    Parameters
    ----------
    cage:FullereneCage
        A planaritable graph of fullerene family.
    sphere_ratio, parr_ratio:float
        ratio to control graph deformation between projection of platform and hemi-sphere.
    projection_point:str
        methods of choosing projection point
        If set to None, it will use the geom-center of the first 6-member circle and average distance away from fullerene center.
        # TODO: Group Point method.
    path:save to file
        if set to None, no file will be saved.

    Returns
    -------

    """
    center_full = np.average(cage.positions, axis=0)  # molecular geom-center

    # projection on a sphere to avoid extrem deformation of shell
    diameter_full = max(np.linalg.norm(cage.positions - center_full, axis=1))  # diameter of sphere to project first time
    pos_sphere = center_full + (cage.positions - center_full) / np.linalg.norm(cage.positions - center_full, axis=1)[:, None] * diameter_full

    # TODO: Group Point method.
    if 1:
        circles = cage.circle_vertex_list
        projection_point_flag = 0
        circle_from = None
        for circle in circles:
            if projection_point>=0:
                if len(circle) == 6:
                    if projection_point_flag == projection_point:
                        circle_from=circle
                        break
                    else:
                        projection_point_flag+=1
            else:
                if len(circle) == 5:
                    if projection_point_flag-1 == projection_point:
                        circle_from=circle
                        break
                    else:
                        projection_point_flag-=1
        if circle_from is None:
            if projection_point>=0:
                raise RuntimeError("No Pentagon found. Please Implement `projection_point` for `planarity_graph_draw` or `projection_circle_idx` for `draw` with `int`<0")
        radius = np.average(np.linalg.norm(pos_sphere[circle_from] - center_full, axis=1))

    center_circle = np.average(cage.positions[circle_from], axis=0)
    project_direct = (center_circle - center_full) / np.linalg.norm((center_circle - center_full))
    center_circle = project_direct * radius

    # get the projection
    pro_radius = max(np.linalg.norm(pos_sphere - center_circle, axis=1))
    project_axis_s = hemisphere_projection_graph(pro_radius, pos_sphere, projection_from=center_circle)

    project_axis_p = parrallel_projection_graph(pro_radius, pos_sphere, projection_from=center_circle, project_direct_parrallel=project_direct)

    # projection from hemisphere to platform
    pro_t = (-project_direct * project_axis_s).sum(-1) - pro_radius - (-project_direct * center_circle).sum(-1)
    project_axis_sp = project_axis_s - pro_t[:, None] * -project_direct
    project_axis_sp = (sphere_ratio * project_axis_sp + parr_ratio * project_axis_p) / 2

    # rotate to XoY
    mx, my, mz = project_direct
    axy = np.sqrt(mx * mx + my * my)
    mat_rotate = np.array([[mx * mz / axy, my * mz / axy, -axy],
                           [-my / axy, mx / axy, 0],
                           [mx, my, mz]])
    project_axis_sp_r = np.einsum("an,mn->am", project_axis_sp, mat_rotate)

    # draw figure
    fig = plt.figure(figsize=[10, 10])
    ax = fig.add_subplot(111)
    # ax.scatter(project_axis_p[:, 0], project_axis_p[:, 1], project_axis_p[:, 2])

    # draw circle and circle fills
    for circleone in circles:
        if len(circleone) == 5:
            xy = [project_axis_sp_r[circleone][:, 0], project_axis_sp_r[circleone][:, 1]]
            ax.add_patch(mpatches.Polygon(np.array(xy).transpose(), color=pentage_color, antialiased=antialiased, alpha=pentage_alpha))

    # draw atoms
    if atom_label:
        ax.scatter(project_axis_sp_r[:, 0], project_axis_sp_r[:, 1], c=line_color, alpha=line_alpha, s=150)
        for i in range(cage.natoms):
            ax.text(project_axis_sp_r[:, 0][i], project_axis_sp_r[:, 1][i], str(i + 1), fontsize=10,
                    horizontalalignment='center',
                    verticalalignment='center', )
            pass
        # draw edge lines
        for edges in cage.graph.edges:
            ax.add_patch(mpatches.FancyArrowPatch(project_axis_sp_r[edges[0]], project_axis_sp_r[edges[1]], antialiased=antialiased, alpha=line_alpha, shrinkA=7, shrinkB=7))
    else:
        ax.scatter(project_axis_sp_r[:, 0], project_axis_sp_r[:, 1], c=line_color, alpha=line_alpha)
        for edges in cage.graph.edges:
            ax.add_patch(mpatches.FancyArrowPatch(project_axis_sp_r[edges[0]], project_axis_sp_r[edges[1]], antialiased=antialiased, alpha=line_alpha, shrinkA=5, shrinkB=5))

    # set the figure
    plt.axis("equal")
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])

    if not path:
        pass
    else:
        fig.savefig(path)
    return ax,project_axis_sp_r

def hemisphere_projection_graph(pro_radius, pos_sphere, projection_from):
    """
    Get projection axis using hemisphere method.
    Parameters
    ----------
    pro_radius:float
        projection length, from `projection_from` point to the projecting surface.
    pos_sphere:np.array
        axis of sphere projection, which can be safely projection using this method without cross lines.
    projection_from:np.array
        projection original point.
    Returns
    -------
    np.array
        hemisphere projection axis.
    """
    pro_vector = pos_sphere - projection_from
    pro_t = pro_radius / np.linalg.norm(pro_vector, axis=1)
    project_axis_s = projection_from + pro_t[:, None] * pro_vector
    return project_axis_s


def parrallel_projection_graph(pro_radius, pos_sphere, projection_from, project_direct_parrallel=np.array([0, 0, 0])):
    """
    Get projection axis using hemisphere method.
    Parameters
    ----------
    pro_radius:float
        projection length, from `projection_from` point to the projecting surface.
    pos_sphere:np.array
        axis of sphere projection, which can be safely projection using this method without cross lines.
    projection_from:np.array
        projection original point.
    project_direct_parrallel:np.array
        projection direction of this parrallel method, also the surface's normal vector (notice the difference as a "-").
    Returns
    -------
    np.array
        hemisphere projection axis.
    """
    pro_vector = pos_sphere - projection_from
    pro_t = pro_radius / (-project_direct_parrallel * pro_vector).sum(-1)
    project_axis_p = projection_from + pro_t[:, None] * pro_vector
    return project_axis_p
