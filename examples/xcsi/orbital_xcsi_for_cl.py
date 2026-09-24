"""
2022/04/24 run for calculating xsi for C60Clm
"""
import ase.neighborlist
import matplotlib.pyplot as plt
import numpy as np
from ase.visualize import view
from tqdm import tqdm

from fullerenedataparser.io.xyz import simple_read_xyz_xtb
from fullerenedataparser.molecular.fullerene import FullereneFamily
import pathlib

np.set_printoptions(threshold=np.inf, linewidth=5000)

SOURCE_DIR = r"E:\archive\DATASETS\FullereneDerivative\Cl\Cl\random\C60_000001812opted"

cage_eig_list = []
eig_list = []
remain_C_list = []
ref_en_list = []
naxx_list = []
napp_list = []

exter_num = 17  # Cl

for optfile in tqdm(list(pathlib.Path(SOURCE_DIR).rglob("xtbopt.xyz"))):
    atoms = list(simple_read_xyz_xtb(optfile))[0]
    natoms = atoms.get_global_number_of_atoms()
    if natoms % 2 == 0:
        nei = ase.neighborlist.NeighborList(ase.neighborlist.natural_cutoffs(atoms))
        nei.update(atoms)
        ADJ = nei.get_connectivity_matrix(sparse=False)
        ADJ = ADJ + ADJ.transpose() - np.diag(np.ones(ADJ.shape[0])) * 2
        idx_cl = []
        idx_cl_c = []
        for idx, is_cl in enumerate(atoms.numbers == exter_num):
            if is_cl:
                idx_cl.append(idx)
        if len(idx_cl) <= 30:
            for idx, is_cl in enumerate(atoms.numbers == exter_num):
                if is_cl:
                    cl_c = ADJ[idx] * np.linspace(0, atoms.get_global_number_of_atoms() - 1, atoms.get_global_number_of_atoms())
                    cl_c[idx_cl] = 0
                    idx_cl_c.append(int((cl_c).sum()))
            n_cl = len(idx_cl)
            ADJ_Cl_C = ADJ[idx_cl_c, :][:, idx_cl_c]  # only C adj with Cl
            ADJ_C = np.delete(ADJ, np.array(idx_cl), 0)  # only C adj
            ADJ_C = np.delete(ADJ_C, np.array(idx_cl), 1)
            XSImatrix = np.delete(ADJ, np.array([*idx_cl, *idx_cl_c]), 0)
            XSImatrix = np.delete(XSImatrix, np.array([*idx_cl, *idx_cl_c]), 1)
            remain_C = XSImatrix.shape[0]
            if remain_C % 2 == 0:
                eig, _ = np.linalg.eigh(ADJ_C)
                cage_eig_list.append(eig)
                naxx_list.append(ADJ_Cl_C.sum() / 2)
                remain_C_list.append(remain_C)
                eig, _ = np.linalg.eigh(XSImatrix)
                eig_list.append(eig)
                ref_en_list.append(atoms.info["energy"])

xxsi_list = []
for idx, item in enumerate(eig_list):
    # xxsi_list.append(np.array(-eig_list[idx][-remain_C_list[idx] // 2:]).sum() + 0.2827 * naxx_list[idx]) #XXSI
    xxsi_list.append(np.array(eig_list[idx][-30:]).sum()-np.array(-eig_list[idx][-remain_C_list[idx] // 2:]).sum() + 0.2827*naxx_list[idx]) #Wang's XSI
xxsi_list = np.array(xxsi_list)
ref_en_list = np.array(ref_en_list)
remain_C_set = set(remain_C_list)
remain_C_list = np.array(remain_C_list)
for remain_class in [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]:
    plt.figure()
    class_idx = np.where(remain_C_list == remain_class)
    if len(class_idx[0]) > 0:
        plt.scatter(xxsi_list[class_idx], ref_en_list[class_idx], marker="x")
        plt.title(f"C60Cl{60 - remain_class}")
        plt.xlabel("xxsi")
        plt.ylabel("xtb Energy/eV")
        plt.tight_layout()
    plt.savefig(f"C60Cl{60 - remain_class}_XSI.pdf")
