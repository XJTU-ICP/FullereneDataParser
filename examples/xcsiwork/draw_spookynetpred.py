# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : draw_spookynetpred.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import pathlib

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
# plt.style.use(["science","nature"])

import numpy as np
from ase.units import mol, kcal, eV, Hartree

from examples.xcsi.utils import charges_draw_parse, charge_name_parse

charged_list = [
    0,
    -2,
    -4,
    -6,
    2,
    4,
    6
]
if __name__ == '__main__':
    draw_list = range(30, 72, 2)
    draw_rc = np.array(list((map(charges_draw_parse, charged_list))))

    for N in draw_list:
        fig = plt.figure(figsize=[8, 8]
                         )
        spec = fig.add_gridspec(ncols=3, nrows=3)
        enref = np.load((pathlib.Path(
            r"C:\Work\CODE\DATA\xcsiwork\spookynetpred") / f"C{N}_spookypred.npz").as_posix())[
                    "xtbenergy_list"] * Hartree / kcal * mol
        for charge in charged_list:
            charge_in_name = charge_name_parse(charge)
            pltidx = charges_draw_parse(charge_number=charge)
            file = (pathlib.Path(
                r"C:\Work\CODE\DATA\xcsiwork\spookynetpred" + charge_in_name) / f"C{N}_spookypred.npz").as_posix()
            file = np.load(file)
            pred_list = file["pred_list"] * eV / kcal * mol
            energy_value = file["xtbenergy_list"]
            min_en = min(energy_value)
            enlist = np.array([item for item in energy_value]) * Hartree / kcal * mol
            xmajorLocator = MaxNLocator("auto",steps=[1, 2, 4, 5, 10],min_n_ticks=3)
            if True:
                if charge == 0:
                    x = pred_list-min(pred_list)
                    y = enlist-min(enlist)
                    ax = fig.add_subplot(spec[0, 0])
                    ax.scatter(x, y, marker="x", color="tab:blue")
                    # ax.set_title(charge_in_name)
                    ax.set_xlabel(r"$E^\mathrm{spooky}_\mathrm{net}$")
                    ax.set_ylabel(r"$E_\mathrm{ref}^\mathrm{xTB}/(\mathrm{kcal\cdot mol^{-1}})$",size=15)
                    ax.text(min(x), max(y) - (max(y) - min(y)) / 10,
                            f"$\mathrm{{C}}_{{{N}}}^{{{str(charge) + '+' if charge > 0 else ('' if charge == 0 else str(-charge) + '-')}}}$",size=15)
                    ax.xaxis.set_major_locator(xmajorLocator)
                    # ax.xaxis.set_major_formatter(xmajorFormatter)
                    ax.autoscale()
                else:
                    x = pred_list-min(pred_list)
                    y = enlist-min(enlist)
                    ax = fig.add_subplot(
                        spec[charges_draw_parse(charge)[0], charges_draw_parse(charge)[
                            1]])
                    if charge > 0:
                        ax.scatter(x, y, marker="x",
                                   color="tab:orange")
                    else:
                        ax.scatter(x, y, marker="x",
                                   color="tab:green")
                    ax.set_xlabel(r"$E^\mathrm{spooky}_\mathrm{net}$")
                    ax.set_ylabel(
                        r"$E_\mathrm{ref_0}^\mathrm{xTB}/(\mathrm{kcal\cdot mol^{-1}})$",size=15)
                    ax.text(min(x), max(y) - (max(y) - min(y)) / 10,
                                f"$\mathrm{{C}}_{{{N}}}^{{{str(charge) + '+' if charge > 0 else ('' if charge == 0 else str(-charge) + '-')}}}$",size=15)
                    ax.xaxis.set_major_locator(xmajorLocator)
                    ax.autoscale()
                plt.tight_layout()
            with open(rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\spookynetpred\Pearson.txt","a") as f:
                corr=np.corrcoef(np.array([pred_list, enlist]))
                print(f"{N} "
                      f"{charge} "
                      f"{corr[1,0]} ",
                      f"{np.square(y - x).mean(axis=-1)}",
                      file=f)
        plt.savefig(
            rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\spookynetpred\C{N}_spookynet.png",
            dpi=600)
        # if N == 60:
        #     ax = fig.add_subplot(spec[0, 1])
        #     ax.get_xaxis().set_visible(False)
        #     ax.get_yaxis().set_visible(False)
        #     ax.axis("off")
        #     skunk.connect(ax, "sk")
        #     svg = skunk.insert({"sk": 'C60.svg'})
        #     with open(
        #             rf"C:\Users\45990\Documents\我的坚果云\draft\2022\xCSI\figures_draft\CSInoNAPP\C{N}_CSI.svg",
        #             "w") as f:
        #         f.write(svg)

