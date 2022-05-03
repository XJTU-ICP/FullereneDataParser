# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : C2addonGenerator.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import os
import sys

import networkx as nx
import numpy as np
import tqdm
from ase.atoms import Atoms
from fullerenedatapraser.graph.algorithm import dual
from fullerenedatapraser.io.recursion import recursion_files
from fullerenedatapraser.io.xyz import simple_read_xyz_xtb
from fullerenedatapraser.molecular.fullerene import FullereneFamily


# script to generate C2 addition patterns.

# pick one cage
def lazy_mkdir(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError as e:
            print(f"It seems you don't hold the target_root_path of {path}.", file=sys.stderr)
            raise e


SOURCE_ROOT = r"D:\CODE\#DATASETS\FullDB\xTBcal\opted"
target_root = r"C:\Users\hanyanbo98\PycharmProjects\FullereneDataPraser\examples\C2addon_simple_edge_index"
CAGE_SEARCH_PATH = r"D:\CODE\usenauty\bin\Release\cagesearch.exe"

TARGET_INFACE_ROOT = r"D:\CODE\#DATASETS\FullDB\C2addon_same_face_index"
lazy_mkdir(TARGET_INFACE_ROOT)
TARGET_ROOT = r"D:\CODE\#DATASETS\FullDB\C2addon"
lazy_mkdir(TARGET_ROOT)

halfC2bond = 0.765
surfaceDis = 1.2


def get_dir_vec(numpyarray):
    assert isinstance(numpyarray, np.ndarray)
    return numpyarray / np.linalg.norm(numpyarray)


def get_one_atoms(num, source_root_path):
    for item in recursion_files(os.path.join(source_root_path, f"C{num}"), ignore_mode=True):
        s_atoms = list(simple_read_xyz_xtb(item))[0]
        yield {"atoms": s_atoms, "name": os.path.splitext(os.path.basename(item))[0]}


class edges_by_nodes:
    def __init__(self, edges, graph: nx.Graph):
        self.edges = [edges_by_nodes(edges[0], graph), edges_by_nodes(edges[1], graph)]

    def get_edge_idx(self):
        pass


tbar = tqdm.tqdm(range(20, 62, 2))
if __name__ == '__main__':

    np.set_printoptions(linewidth=500)
    for i in tbar:
        for result in get_one_atoms(num=i, source_root_path=SOURCE_ROOT):
            tbar.set_description(f"Working on atom {i}, file {result['name']}")
            s_atoms = result["atoms"]
            filename = result["name"]
            oneoutputfile = os.path.abspath(os.path.join(target_root, f'C{i}', f'{filename}.out'))
            fuller = FullereneFamily(spiral=0, atoms=s_atoms)
            G: nx.Graph = fuller.graph()
            edgeslist = list(G.edges)
            n_edges = len(edgeslist)
            edges = np.array(edgeslist)
            dual_gen = dual.py_graph_circle_finder(n_edges, edges.data)
            facelist = dual_gen.get_face_vertex_list()
            edgeslist = list(G.edges)
            if not os.path.exists(oneoutputfile):
                tbar.set_postfix(status=f"Edge Nauty, file {oneoutputfile} is generating...")
                E_ADJ = np.zeros([n_edges, n_edges])
                for edge in edgeslist:
                    edgeidx_1 = edgeslist.index(edge)
                    for node in edge:
                        edgeofnode = G.edges(node)
                        for edge2 in edgeofnode:
                            if edge2[0] > edge2[1]:
                                edge2 = (edge2[1], edge2[0])
                            edgeidx_2 = edgeslist.index(edge2)
                            if edgeidx_1 != edgeidx_2:
                                E_ADJ[edgeidx_1][edgeidx_2] = 1
                E_graph = nx.from_numpy_matrix(E_ADJ)
                graph6str = nx.to_graph6_bytes(E_graph, header=False).decode().split()[0]
                lazy_mkdir(os.path.abspath(os.path.join(target_root, f'C{i}')))
                os.system(f"{CAGE_SEARCH_PATH} --graph6str \"{graph6str}\" --addnum 2 -o \"{oneoutputfile}\"")
            tbar.set_postfix(status=f"Edge Nauty, file {oneoutputfile} is exist.")
            # addon generate
            addon_face_index_file_path = os.path.join(TARGET_INFACE_ROOT, filename)
            if not os.path.exists(addon_face_index_file_path):
                tbar.set_postfix(f"Edge filter, file {addon_face_index_file_path} is generating...")
                addon_face_index_file = open(addon_face_index_file_path, "w")
                with open(oneoutputfile, "r") as f:
                    for item in f.readlines():
                        edgeidx_1, edgeidx_2 = item.split()
                        edge1 = edgeslist[int(edgeidx_1)]
                        edge2 = edgeslist[int(edgeidx_2)]
                        # print(edge1,edge2)
                        # print(facelist)
                        bothinfaceflag = False
                        for face in facelist:
                            if edge1[0] in face:
                                if edge1[1] in face:
                                    if edge2[0] in face:
                                        if edge2[1] in face:
                                            bothinfaceflag = True
                                            break
                        # print(bothinfaceflag)
                        if bothinfaceflag:
                            print(f"{int(edgeidx_1):3d} {int(edgeidx_2):3d}", file=addon_face_index_file)
                addon_face_index_file.close()
            tbar.set_postfix(status=f"Edge filter, file {addon_face_index_file_path} is exist.")
            # generate new xyz, calculate and phrase
            with open(addon_face_index_file_path, "r") as f:
                tbar.set_postfix(status=f"C2adding, on file {addon_face_index_file_path}. Starting...")
                TARGET_ROOT_FILE_PATH = os.path.join(TARGET_ROOT, filename)
                lazy_mkdir(TARGET_ROOT_FILE_PATH)
                TARGET_ROOT_TABLE_PATH = os.path.join(TARGET_ROOT, filename, "addonlist")
                table_file = open(TARGET_ROOT_TABLE_PATH, "w")
                addontypeflag = 1
                for addon_pattern in f.readlines():
                    edgeidx_1, edgeidx_2 = addon_pattern.split()
                    edge1 = edgeslist[int(edgeidx_1)]
                    edge2 = edgeslist[int(edgeidx_2)]
                    notbesidesflag = True
                    for node1 in edge1:
                        if node1 in edge2:
                            notbesidesflag = False
                            break
                    if notbesidesflag:
                        tbar.set_postfix(status=f"C2adding, on file {addon_face_index_file_path}. Adding {addontypeflag}th one.")
                        edge1c = fuller.positions[edge1, :].sum(axis=0) / 2
                        edge2c = fuller.positions[edge2, :].sum(axis=0) / 2
                        surfcenter = (edge1c + edge2c) / 2
                        bonddirect = get_dir_vec(edge1c - surfcenter)
                        surfdirect = get_dir_vec(surfcenter - np.average(fuller.positions, axis=0))
                        c2bondc = surfcenter + surfdirect * surfaceDis
                        carbon1pos = c2bondc + bonddirect * halfC2bond
                        carbon2pos = c2bondc - bonddirect * halfC2bond
                        newatoms = Atoms(numbers=[6 for _ in range(fuller.natoms + 2)],
                                         positions=list([*fuller.positions, carbon1pos, carbon2pos]))
                        newatoms.write(os.path.join(TARGET_ROOT_FILE_PATH, f"{filename}_c2add_{addontypeflag:03d}.xyz"), format="xyz")
                        print(f"#{addontypeflag}# {int(edgeidx_1):3d} {int(edgeidx_2):3d}", file=table_file)
                        addontypeflag += 1
                table_file.close()

        # check and output
