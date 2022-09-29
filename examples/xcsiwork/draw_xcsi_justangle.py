# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : draw_csi_nonapp.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import pathlib

import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
# plt.rc('font', family='Times New Roman')
# plt.style.use(["science","nature"])

import numpy as np
from ase.units import mol, kcal, Hartree
import matplotlib.image as mpimg
from matplotlib.ticker import MaxNLocator

from examples.xcsi.utils import charges_draw_parse, charge_name_parse, \
    calculate_xcsi

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
            r"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\data\xCSI_justangle") / f"C{N}_xCSI_justangle.npz").as_posix())[
                    "energy"] * Hartree / kcal * mol
        for charge in charged_list:
            charge_in_name = charge_name_parse(charge)
            pltidx = charges_draw_parse(charge_number=charge)
            file = (pathlib.Path(
                r"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\data\xCSI_justangle" + charge_in_name) / f"C{N}_xCSI_justangle.npz").as_posix()
            file = np.load(file)
            csi_value = file["csi_list"]
            energy_value = file["energy"]
            min_en = min(energy_value)
            napp_value = file['napp']

            evallist = calculate_xcsi(csi_value, None, charge)
            enlist = np.array([item for item in energy_value]) * Hartree / kcal * mol
            xmajorLocator = MaxNLocator("auto",steps=[1, 2, 4, 5, 10],min_n_ticks=3)
            # xmajorFormatter = FormatStrFormatter('%5.2f')
            if True:
                if charge == 0:
                    x = evallist
                    y = enlist - min(enlist)
                    ax = fig.add_subplot(spec[0, 0])
                    ax.scatter(x, y, marker="x", color="tab:blue")
                    ax.tick_params(which='major', width=1.00, length=5)
                    ax.tick_params(which='minor', width=0.75, length=2.5)
                    # ax.set_title(charge_in_name)
                    ax.set_xlabel(r"$E^\mathrm{angle,nodis}_\mathrm{XCSI}$", size=15)
                    ax.set_ylabel(
                        r"$E_\mathrm{ref}^\mathrm{xTB}/(\mathrm{kcal\cdot mol^{-1}})$",
                        size=15)
                    ax.text(min(x), max(y) - (max(y) - min(y)) / 10,
                            f"$\mathrm{{C}}_{{{N}}}^{{{str(charge) + '+' if charge > 0 else ('' if charge == 0 else str(-charge) + '-')}}}$",
                            size=15)
                    ax.xaxis.set_major_locator(xmajorLocator)
                    ax.autoscale()
                else:
                    x = evallist
                    y = enlist - min(enlist)
                    ax = fig.add_subplot(
                        spec[charges_draw_parse(charge)[0], charges_draw_parse(charge)[
                            1]])
                    ax.tick_params(which='major', width=1.00, length=5)
                    ax.tick_params(which='minor', width=0.75, length=2.5)
                    if charge > 0:
                        ax.scatter(x, y, marker="x",
                                   color="tab:orange")
                    else:
                        ax.scatter(x, y, marker="x",
                                   color="tab:green")
                    ax.set_xlabel(r"$E^\mathrm{angle,nodis}_\mathrm{XCSI}$", size=15)
                    ax.set_ylabel(
                        r"$E_\mathrm{ref}^\mathrm{xTB}/(\mathrm{kcal\cdot mol^{-1}})$",
                        size=15)
                    ax.text(min(x), max(y) - (max(y) - min(y)) / 10,
                            f"$\mathrm{{C}}_{{{N}}}^{{{str(charge) + '+' if charge > 0 else ('' if charge == 0 else str(-charge) + '-')}}}$",
                            size=15)
                    ax.xaxis.set_major_locator(xmajorLocator)
                    # ax.xaxis.set_major_formatter(xmajorFormatter)
                    ax.autoscale()
                plt.tight_layout()
                ax = fig.add_subplot(spec[0, 1:])
                img = mpimg.imread("xcsianglenodis.png")
                ax.set_axis_off()
                ax.imshow(img, )
            with open(rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\xCSI_justangle\Pearson.txt","a") as f:
                corr=np.corrcoef(np.array([evallist, enlist]))
                print(f"{N} "
                      f"{charge} "
                      f"{corr[1,0]}",
                      file=f)
        plt.savefig(
            rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\xCSI_justangle\C{N}_justangle.png",
            dpi=600)
        # if N == 60:
        #     ax = fig.add_subplot(spec[0, 1])
        #     ax.get_xaxis().set_visible(False)
        #     ax.get_yaxis().set_visible(False)
        #     ax.axis("off")
        #     skunk.connect(ax, "sk")
        #     svg = skunk.insert({"sk": 'C60.svg'})
        #     with open(
        #             rf"C:\Users\45990\Nutstore\1\我的坚果云\draft\2022\xCSI\figures_draft\CSInoNAPP\C{N}_CSI.svg",
        #             "w") as f:
        #         f.write(svg)