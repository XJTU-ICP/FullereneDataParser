# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : _pyscf.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np
import pandas as pd
from ase import Atoms
from pyscf import gto

mol1 = gto.M(atom='C 0 0 0; C 1.0 1.0 0; C 1.0 0 0', basis='STO-3G')
mol2 = gto.M(atom='C 0 0 0; C 1.0 0 0', basis='STO-3G')

ethane = gto.M(atom="C                  0.0000000 -0.0000000  0.762552;"
                    "H                  0.0000000  1.018547   1.158777;"
                    "H                  0.8820876 -0.5092735  1.158777;"
                    "H                 -0.8820876 -0.5092735  1.158777;"
                    "C                  0.         0.        -0.762552;"
                    "H                 -0.        -1.018547  -1.158777;"
                    "H                  0.8820876  0.5092735 -1.158777;"
                    "H                 -0.8820876  0.5092735 -1.158777;",
               charge=0,
               spin=0,
               # basis="ccpvdz")
               basis="STO-3G")
ethylene = gto.M(atom="C                  -0.         0.         0.6604068;"
                      "H                   0.9223709  0.         1.2295378;"
                      "H                  -0.9223709 -0.         1.2295378;"
                      "C                  -0.        -0.        -0.6604068;"
                      "H                   0.9223709  0.        -1.2295378;"
                      "H                  -0.9223709  0.        -1.2295378;",
                 charge=0,
                 spin=0,
                 # basis="ccpvdz")
                 basis="STO-3G")


# mf = scf.RHF(ethylene)
# mol_eq = optimize(mf)
# pos = mol_eq.atom_coords()
# atom = Atoms(numbers=[6, 1, 1, 6, 1, 1], positions=pos)
#
# methane_eq = gto.M(atom="".join([f"{atom.symbols[i]} {atom.positions[i][0]} {atom.positions[i][1]} {atom.positions[i][2]};" for i in range(6)]))
#
# print(np.around((pos-pos.sum()/6) * Bohr / Angstrom, 7))

# hcore = mol1.intor('int1e_nuc_sph') + mol1.intor('int1e_kin_sph')
# overlap = mol1.intor('int1e_ovlp_sph')
# eri = mol1.intor('int2e_sph')
# pprint(mol1.ao_labels())
# pprint(methane.ao_labels())

# np.set_printoptions(linewidth=1000)
# np.set_printoptions(threshold=np.inf)


def print_int1e(mol, obitals):
    print([mol.cart_labels()[i] for i in obitals])
    print("ovlp", mol.intor("int1e_ovlp")[obitals])
    print("kin", mol.intor("int1e_kin")[obitals])


# orbital2p = [(num, item) for num, item in enumerate(ethylene.cart_labels()) if "2" in item]
# [print_int1e(ethylene, orbitals) for orbitals in product([item[0] for item in orbital2p], [item[0] for item in orbital2p])]

def get_labels_index(mol, labels):
    for target_label in labels:
        for idx, label in enumerate(mol.cart_labels()):
            if target_label in label:
                yield idx


def get_one_intor(molintor, label1, label2):
    return molintor[label1, label2]


def loop_mol(thetas, phis, ds, baseset="STO-3G"):
    intor_np = []
    for theta in thetas:
        for phi in phis:
            for d in ds:
                pos = np.array([[0, 0, d / 2],
                                [0.9223709, 0, 1.2295378],
                                [-0.9223709, 0, 1.2295378],
                                [0, 0, -d / 2],
                                [0.9223709, 0, -1.2295378],
                                [-0.9223709, 0, -1.2295378]])
                mol = Atoms(numbers=[6, 1, 1, 6, 1, 1], positions=pos)
                mol.rotate(theta, "y")
                mol.rotate(phi, "z")
                # print(f"theta:{theta}, phi:{phi}, d:{d}:")
                ethylene_one = gto.M(atom="".join([f"{mol.symbols[i]} {mol.positions[i][0]} {mol.positions[i][1]} {mol.positions[i][2]};" for i in range(6)]),
                                     charge=0,
                                     spin=0,
                                     # basis="ccpvdz")
                                     basis=baseset)
                for label1 in get_labels_index(ethylene_one, ["0  C 2s", "3  C 2s"]):
                    for label2 in get_labels_index(ethylene_one, ["0  C 2s", "3  C 2s"]):
                        intor_np.append(get_one_intor(ethylene_one.intor("int1e_kin"), label1, label2) / get_one_intor(ethylene_one.intor("int1e_ovlp"), label1, label2))

    pd.DataFrame()


loop_mol(np.arange(0, 91, 15), np.arange(0, 91, 15), ds=np.arange(1, 2, 0.1), baseset="STO-3G")
