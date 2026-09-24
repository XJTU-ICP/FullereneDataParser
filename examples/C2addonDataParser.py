# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : C2addonDataParser.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import os
from tqdm import tqdm

import dpdata
from dpdata.system import load_format
from glob import glob
# cage_grad_data_dir = r"D:\CODE\#DATASETS\FullDB\xTBGrad"
C2addon_cage_dir=r"D:\CODE\#DATASETS\FullDB\C2addon"
tbar = tqdm()
origin_ms = dpdata.MultiSystems()
# origin_ms = origin_ms.from_dir(r"D:\CODE\#DATASETS\dpdata_xtbopt",file_name="",fmt="deepmd/npy",recursive=False)

ms = dpdata.MultiSystems()
for item in range(20,56,2):
    subdir = f"C{item}"
    if subdir in origin_ms.systems:
        continue
    # whole_cage_grad_data_dir = os.path.join(cage_grad_data_dir,subdir)
    whole_cage_grad_data_dir = C2addon_cage_dir+str(f"/{subdir}*")
    # if not os.path.exists(whole_cage_grad_data_dir):
    #     continue
    filelist = glob(whole_cage_grad_data_dir+r"/*.gradient",recursive=True)
    tbar.set_description(f"Working on {subdir}")
    tbar.reset(total=len(filelist))
    ls = dpdata.LabeledSystem()
    for onegrad in filelist:
        tbar.set_description(f"Working on {subdir}/{onegrad}")
        ls.append(dpdata.LabeledSystem(file_name=onegrad, fmt='xtb/gradient',type_map=["C"]))
        tbar.update()
    ms.append(ls)

ms.to_deepmd_npy(r"D:\CODE\#DATASETS\dpdata_c2addon")


# xtb_grad_multi_systems = dpdata.MultiSystems.from_dir(dir_name=GRAD_FILE_DIR, file_name='*.grad', fmt='xtb/gradient',type_map=["C"])
# xtb_grad_multi_systems.systems["C20"].to_deepmd_npy("dpdata_examp")
