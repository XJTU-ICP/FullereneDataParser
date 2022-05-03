# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : origin_csi.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

__doc__ = """
# ================ NOTE ================ #
# Request packages: `numpy`,`matplotlib`
# 1. Setup data source.
# 2. Calculate if needed.
# 3. Draw images of data.
# ================ NOTE ================ #
"""

import pathlib
import matplotlib.pyplot as plt
import numpy as np
from functools import partial

import pandas as pd
import seaborn as sns

from fullerenedatapraser.calculator.extend_csi import mp_store_csi, calculate_ext_csi
from utils import charge_name_parse, charges_draw_parse, calculate_origin_csi, calculate_origin_csi_without_napp, calculate_origin_csi_only_napp, calculate_xcsi

plt.rcParams['font.sans-serif'] = "Arial"

if __name__ == '__main__':
    _ = \
        """
    # =============== PART 1 ================ #
    1. Setup data source.
    
    SPIRAL_ATOMS_ADJ_DIR:
        Directory storing output files of `spiral` program.
        As an example, file `C20` is:
    >   # General fullerene of C20:
    >       <spiral ID> <PG> <Pentagon index> <NMR>
    >       <ADJ matrix, shape [20,20]>
    >       ...
    
    SPIRAL_CIRCLE_ADJ_DIR:
        Directory storing output files of `spiral` program.
        As an example, file `C20` is:
    >   # General fullerene of C20:
    >       <spiral ID> <PG> <Pentagon index> <NMR>
    >       <ADJ matrix of circles, shape [12,12]>
    >       ...
    
    XYZ_STORE_PREFIX:
        Prefix name of Directory storing files of C<2N> coordinates particularly.
        Directory structure should be:
            XYZ_STORE_PREFIX_<...>
            |-C20
            | |-C20_000000001opt.xyz
            | ...
            |-C24
            |...
        
        These .xyz files have energy calculated by `xTB`.
        As an example, file `C20_000000001opt.xyz` is:
    >   20
    >    energy: -42.0890 <info>
    >   C  <xyz coordinates>
    >   ...
    
    CSI_NPY_STORE_PREFIX:
        Prefix name of Directory storing files of C<2N>  particularly.    
        See `numpy.load()` and `numpy.savez()` for details.
        Each `.npz` file have three `numpy.array()` named:
        ['csi_list', 'spiral_num', 'energy', 'napp']
        CSI_NPY_STORE_PREFIX<...>
            |-C20_CSI.npz
            |-C24_CSI.npz
            |...
    
    # =============== PART 1 ================ #
    """
    DIS_CUT = None
    calculate_ext_csi = partial(calculate_ext_csi, distance_cutoff=DIS_CUT)
    SPIRAL_ATOMS_ADJ_DIR = r"D:\CODE\#DATASETS\FullDB\atomadj"  # change this
    SPIRAL_CIRCLE_ADJ_DIR = r"D:\CODE\#DATASETS\FullDB\circleadj"  # change this
    XYZ_STORE_PREFIX = r"D:\CODE\#DATASETS\FullDB\xTBcal"  # change this
    CSI_NPY_STORE_PREFIX = r"D:\CODE\#DATASETS\FullDB\c2addonwork\xCSI7_all" + str(DIS_CUT)  # change this
    if not pathlib.Path(XYZ_STORE_PREFIX).exists():
        pathlib.Path(XYZ_STORE_PREFIX).mkdir(parents=True)
    if not pathlib.Path(CSI_NPY_STORE_PREFIX).exists():
        pathlib.Path(CSI_NPY_STORE_PREFIX).mkdir(parents=True)

    charged_list = [
        0,
        -2,
        -4,
        -6,
        2,
        4,
        6
    ]

    CSI_NPY_FILE_SUFFIX = "xCSI" + str(DIS_CUT)
    _ = \
        """
    # =============== PART 2 ================ #
    2. Calculate if needed.
    Set `_recalculate` = `True` if force to recalculate all data.
    
    # =============== PART 2 ================ #
    """
    _recalculate = False  # set to True to recalculate all

    _pass = False  # set to True to force pass calculation

    include_traj = True  # set to `False` to only calculate the optimized isomers (most stable configurations)

    number_mask = range(60, 62, 10)
    # Set to None if not need mask
    print("Calculating...")
    if not _pass:
        for charge in charged_list:
            charge_in_name = charge_name_parse(charge)
            if _recalculate:
                print("Recalculate all without any delete, be careful.")
                mp_store_csi(atomdir=SPIRAL_ATOMS_ADJ_DIR,
                             circledir=SPIRAL_CIRCLE_ADJ_DIR,
                             xyz_root_dir=XYZ_STORE_PREFIX + charge_in_name,
                             target_dir=CSI_NPY_STORE_PREFIX + charge_in_name,
                             number_mask=number_mask,
                             npz_file_suffix=CSI_NPY_FILE_SUFFIX,
                             _func=calculate_ext_csi,
                             include_traj=include_traj)
            else:
                mp_store_csi(atomdir=SPIRAL_ATOMS_ADJ_DIR,
                             circledir=SPIRAL_CIRCLE_ADJ_DIR,
                             xyz_root_dir=XYZ_STORE_PREFIX + charge_in_name,
                             target_dir=CSI_NPY_STORE_PREFIX + charge_in_name,
                             npz_file_suffix=CSI_NPY_FILE_SUFFIX,
                             number_mask=number_mask,
                             recalculate=False,
                             _func=calculate_ext_csi,
                             include_traj=include_traj)
    print("Calculated.")
    _ = \
        """
    # =============== PART 3 ================ #
    3. Calculate if needed.
    

    # =============== PART 2 ================ #
    """
    draw_list = range(60, 62, 10)
    draw_rc = np.array(list((map(charges_draw_parse, charged_list))))

    napp_value_all = np.array([])
    xcsilist_only_xcsi_all = np.array([])
    enlist_all = np.array([])
    charge_all = np.array([])
    print("Drawing...")
    for N in draw_list:
        # fig, ax = plt.subplots(nrows=3, ncols=max(draw_rc[:, 1]) + 1)
        for charge in charged_list:
            charge_in_name = charge_name_parse(charge)
            pltidx = charges_draw_parse(charge_number=charge)
            file = (pathlib.Path(CSI_NPY_STORE_PREFIX + charge_in_name) / f"C{N}_{CSI_NPY_FILE_SUFFIX}.npz").as_posix()
            file = np.load(file)
            csi_value = file["csi_list"]
            energy_value = file["energy"]
            min_en = min(energy_value)
            napp_value = file['napp']
            # set `napp_value` to None to use xcsi without napp values.
            xcsilist = calculate_xcsi(csi_value, napp_value, charge)
            xcsilist_only_xcsi = calculate_xcsi(csi_value, None, charge)
            enlist = [item for item in energy_value]
            # ax[pltidx[0], pltidx[1]].scatter(xcsilist, enlist, marker="x")
            # ax[pltidx[0], pltidx[1]].set_xlabel("XCSI of {} isomers, cutoff={}".format(f"C$_{{{N}}}^{{{str(charge) + '+' if charge > 0 else '' if charge >= 0 else str(abs(charge)) + '-'}}}$", DIS_CUT))
            # ax[pltidx[0], pltidx[1]].set_ylabel("Relative energy of {} isomers".format(f"C$_{{{N}}}^{{{str(charge) + '+' if charge > 0 else '' if charge >= 0 else str(abs(charge)) + '-'}}}$", DIS_CUT))
            # print(charge, np.corrcoef(np.array([xcsilist, napp_value, xcsilist_only_xcsi, enlist])))
            napp_value_all = np.hstack([napp_value_all, napp_value])
            xcsilist_only_xcsi_all = np.hstack([xcsilist_only_xcsi_all, xcsilist_only_xcsi])
            enlist_all = np.hstack([enlist_all, enlist])
            charge_all = np.hstack([charge_all, np.ones_like(enlist) * charge])

        data = pd.DataFrame(data={
            "napp_value": napp_value_all, "xcsilist_only_xcsi": xcsilist_only_xcsi_all, "enlist": enlist_all, "charge": charge_all
        })
        g = sns.scatterplot(data=data, x="xcsilist_only_xcsi", y="enlist", hue="charge")
        g.set_xlabel("XCSI")
        g.set_ylabel("$E_\mathrm{r}$/eV")
plt.show()
