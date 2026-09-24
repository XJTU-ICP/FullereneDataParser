# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : post_pearson.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import numpy as np

Pearson_Data_Path = r"E:\我的坚果云\draft\2022\xCSI\figures_draft\xCSI_POAV\Pearson.txt"

data = {

}

with open(Pearson_Data_Path, "r") as f:
    for line in f.readlines():
        item = line.split()
        num = str(item[0])
        charge = item[1]
        pearson = item[2]
        if data.get(num, None) is None:
            data[num] = {}
        data[num][charge] = np.round_(float(pearson), 2)

for i in range(30,72,2):
    num = str(i)
    print(f"{num}&{data[num]['0']}&{data[num]['-2']}&{data[num]['-4']}&{data[num]['-6']}&{data[num]['2']}&{data[num]['4']}&{data[num]['6']}\\\\")