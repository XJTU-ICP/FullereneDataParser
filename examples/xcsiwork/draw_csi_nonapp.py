# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : draw_csi_nonapp.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import pathlib

import matplotlib.pyplot as plt
from matplotlib import rcParams, image as mpimg
import skunk
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator
from tqdm import tqdm

from src.fullerenedatapraser.molecular.fullerene import FullereneCage

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
# plt.rc('font', family='Times New Roman')
# plt.style.use(["science","nature"])

import numpy as np
from ase.units import mol, kcal, eV, Hartree

from examples.xcsi.utils import charges_draw_parse, charge_name_parse, \
    calculate_origin_csi_only_napp, calculate_origin_csi, \
    calculate_origin_csi_without_napp, calculate_xcsi

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
            r"C:\Work\CODE\DATA\xcsiwork\CSI") / f"C{N}_CSI.npz").as_posix())[
                    "energy"] * Hartree / kcal * mol
        for charge in charged_list:
            charge_in_name = charge_name_parse(charge)
            pltidx = charges_draw_parse(charge_number=charge)
            file = (pathlib.Path(
                r"C:\Work\CODE\DATA\xcsiwork\CSI" + charge_in_name) / f"C{N}_CSI.npz").as_posix()
            file = np.load(file)
            csi_value = file["csi_list"]
            energy_value = file["energy"]
            min_en = min(energy_value)
            napp_value = file['napp']

            napplist = calculate_origin_csi_only_napp(csi_value, napp_value, charge)
            csilist = calculate_origin_csi(csi_value, napp_value, charge)
            evallist = calculate_origin_csi_without_napp(csi_value, napp_value, charge)
            allhalflist = calculate_xcsi(csi_value, None, charge)
            enlist = np.array([item for item in energy_value]) * Hartree / kcal * mol
            alphabetlabel = [['a'],['b','c','d'],['e','f','g']]
            xmajorLocator = MaxNLocator("auto",steps=[1, 2, 4, 5, 10],min_n_ticks=3)
            if True:
                if charge == 0:
                    x = napplist
                    y = enlist - min(enlist)
                    ax = fig.add_subplot(spec[0, 0])
                    ax.scatter(x, y, marker="x", color="tab:blue")
                    # ax.set_title(charge_in_name)
                    ax.set_xlabel(r"$0.2\mathrm{NAPP}$",size=15)
                    ax.set_ylabel(r"$E_\mathrm{ref}^\mathrm{xTB}/(\mathrm{kcal\cdot mol^{-1}})$",size=15)
                    ax.text(min(x), max(y) - (max(y) - min(y)) / 6,
                            rf"$\mathbf{{({alphabetlabel[charges_draw_parse(charge)[0]][charges_draw_parse(charge)[1]]})}}\mathrm{{C}}_{{{N}}}^{{{str(charge) + '+' if charge > 0 else ('' if charge == 0 else str(-charge) + '-')}}}$",size=15)
                    ax.xaxis.set_major_locator(xmajorLocator)
                    # ax.xaxis.set_major_formatter(xmajorFormatter)
                    ax.autoscale()
                else:
                    x = evallist
                    y = enlist - enref
                    ax = fig.add_subplot(
                        spec[charges_draw_parse(charge)[0], charges_draw_parse(charge)[
                            1]])

                    if charge > 0:
                        ax.scatter(x, y, marker="x",
                                   color="tab:orange")
                    else:
                        ax.scatter(x, y, marker="x",
                                   color="tab:green")
                    ax.set_xlabel(r"$X^q_i$", size=15)
                    ax.set_ylabel(
                        r"$E_\mathrm{ref_0}^\mathrm{xTB}/(\mathrm{kcal\cdot mol^{-1}})$",size=15)
                    ax.text(min(x), max(y) - (max(y) - min(y)) / 6,
                                rf"$\mathbf{{({alphabetlabel[charges_draw_parse(charge)[0]][charges_draw_parse(charge)[1]]})}}\mathrm{{C}}_{{{N}}}^{{{str(charge) + '+' if charge > 0 else ('' if charge == 0 else str(-charge) + '-')}}}$",size=15)
                    ax.xaxis.set_major_locator(xmajorLocator)
                    # ax.xaxis.set_major_formatter(xmajorFormatter)
                    ax.autoscale()
                plt.tight_layout()
                ax = fig.add_subplot(spec[0, 1:])
                img = mpimg.imread("csinonapp.png")
                ax.set_axis_off()
                ax.imshow(img,)
            with open(rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\CSInoNAPP\Pearson.txt","a") as f:
                corr=np.corrcoef(np.array([napplist, evallist, enlist - enref]))
                print(f"{N} "
                      f"{charge} "
                      f"{corr[2,1] if charge else np.corrcoef(np.array([napplist,enref]))[0,1]}",
                      file=f)
        plt.savefig(
            rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\CSInoNAPP\C{N}_CSI.png",
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
