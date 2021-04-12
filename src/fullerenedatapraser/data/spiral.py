# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : spiral.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import re

import numpy as np
import pandas as pd
from fullerenedatapraser.util.logger import Logger

logger = Logger(__name__, console_on=True)


class SpiralFile:
    """
    Class of files for spiral output.
    """
    regex_int_name = re.compile(r"\d+")

    def __init__(self, path: str, atom_num: int = None, circle: bool = False):
        """

        Parameters
        ----------
        path:str
            Path string of spiral file.
        atom_num:int
            Atom number of carbon atoms spiral file. Optional.
        circle:bool
            File is content of circle or not. Default to atom adjacent.
        """
        self.path = path
        self.circle = circle
        if atom_num:
            self.atom_num = atom_num
        else:
            try:
                self.atom_num = int(SpiralFile.regex_int_name.findall(path)[-1])
            except AttributeError:
                logger.warning("Not a typical path of spiral file. I'll try reading from the file.")
                self.read_atom_from_file = True
            except Exception:
                raise Exception
        self.file = open(path, "r")
        self._read_first_line()

    def _read_first_line(self):
        firstline = self.file.readline()
        if firstline.startswith("# General fullerene of C"):
            if getattr(self, "read_atom_from_file", False):
                pass
        else:
            logger.error(f"Wrong spiral file, the first line is {firstline}.")
            raise ValueError
        if not self.circle:
            self.atom_num = int(SpiralFile.regex_int_name.findall(firstline)[-1])
        else:
            self.atom_num = int(SpiralFile.regex_int_name.findall(firstline)[-1]) // 2 + 2

    def _read_body(self):
        self.spiral_num_line = True
        self.axis_lines = 0
        self.spiral_num = 0
        self.adj_matrix = np.zeros([self.atom_num, self.atom_num], dtype=int)
        for self.line in self.file.readlines():
            content = self._read_spiral_num()
            if content:
                yield content
            else:
                pass

    def content(self):
        """

        Returns
        -------
        Generator:
            {
                "spiral_num": spiral_num,
                "adj_matrix": adj_matrix,
                "symmetry": symmetry,
                "pentagon_index": pentagon_index,
                "NMR": NMR
            }

        """
        return self._read_body()

    def _read_spiral_num(self):
        if self.line.startswith(" ") and self.spiral_num_line:  # Case: at spiral number line
            self._before_spiral_number_line_hook()
            self.spiral_num_line = False
            self.spiral_num += 1
            self.spiral_num_line_info = list(self.line.split())
            assert self.spiral_num == int(self.spiral_num_line_info[0])
            self.symmetry = self.spiral_num_line_info[1]
            self.pentagon_index = [int(i) for i in self.spiral_num_line_info[2:14]]
            self.NMR = "".join(self.spiral_num_line_info[14:])
            self._after_spiral_number_line_hook()
        elif not self.spiral_num_line:  # Case: at coordination lines.
            if self.axis_lines < self.atom_num:  # Case: not at the end.
                self.adj_matrix[self.axis_lines] = np.array([int(i) for i in self.line.split()])
                self.axis_lines += 1
            if self.axis_lines == self.atom_num:  # Case: end line of matrix.
                self.spiral_num_line = True
                self.axis_lines = 0
                self._after_matrix_hook()
                return {
                    "spiral_num": self.spiral_num,
                    "adj_matrix": self.adj_matrix,
                    "symmetry": self.symmetry,
                    "pentagon_index": self.pentagon_index,
                    "NMR": self.NMR
                }
            if self.axis_lines > self.atom_num:
                raise ValueError(f"Runtime Error: Wrong lines count in file {self.path} with lines number got {self.axis_lines}.")

    def _before_spiral_number_line_hook(self):
        self.before_spiral_number_line_hook()

    def before_spiral_number_line_hook(self):
        pass

    def _after_spiral_number_line_hook(self):
        self.after_spiral_number_line_hook()

    def after_spiral_number_line_hook(self):
        pass

    def _after_matrix_hook(self):
        self.after_matrix_hook()

    def after_matrix_hook(self):
        pass


def read_atomadj(path):
    with open(path, "r"):
        SF = SpiralFile(path)
        return SF.content()


def read_circleadj(path):
    with open(path, "r"):
        SF = SpiralFile(path, circle=True)
        return SF.content()


def adj_store(path, gener, buffer=1000):
    spiral_num = []
    symmetry = []
    NMR = []
    atomadj = []
    circleadj = []
    pentagon_index = []
    df = pd.DataFrame(
        columns=[
            "spiral_num",
            "symmetry",
            "NMR",
            "atomadj",
            "circleadj",
            "pentagon_index"
        ]
    )
    store_flag = False
    for count, item in enumerate(gener, 1):
        spiral_num.append(item["spiral_num"])
        symmetry.append(item["symmetry"])
        NMR.append(item["NMR"])
        atomadj.append(item["atomadj"])
        circleadj.append(item["circleadj"])
        pentagon_index.append(item["pentagon_index"])
        if count % buffer == 0:
            store_flag = True
        else:
            store_flag = False
        if store_flag:
            df_one = pd.DataFrame(
                columns=[
                    "spiral_num",
                    "symmetry",
                    "NMR",
                    "pentagon_index",
                    "atomadj",
                    "circleadj"
                ],
                data={
                    "spiral_num": np.array(spiral_num),
                    "symmetry": symmetry,
                    "NMR": NMR,
                    "pentagon_index": pentagon_index,
                    "atomadj": atomadj,
                    "circleadj": circleadj
                }
            )
            df = df.append(df_one, ignore_index=True)
            df.to_hdf(path, 'spiral')
            spiral_num = []
            symmetry = []
            NMR = []
            atomadj = []
            circleadj = []
            pentagon_index = []
    df_one = pd.DataFrame(
        columns=[
            "spiral_num",
            "symmetry",
            "NMR",
            "pentagon_index",
            "atomadj",
            "circleadj"
        ],
        data={
            "spiral_num": np.array(spiral_num),
            "symmetry": symmetry,
            "NMR": NMR,
            "pentagon_index": pentagon_index,
            "atomadj": atomadj,
            "circleadj": circleadj
        }
    )
    df = df.append(df_one, ignore_index=True)
    df.to_hdf(path, 'spiral')
    logger.info(f"ADJ infomation has been stored in {path}.")


def adj_gener(atomfile, circlefile):
    atomadj = read_atomadj(atomfile)
    circleadj = read_circleadj(circlefile)
    for atom in atomadj:
        circle = next(circleadj)
        if atom["spiral_num"] == circle["spiral_num"]:
            pass
        else:
            raise ValueError
        yield {
            "spiral_num": atom["spiral_num"],
            "atomadj": atom["adj_matrix"],
            "symmetry": atom["symmetry"],
            "pentagon_index": atom["pentagon_index"],
            "circleadj": circle["adj_matrix"],
            "NMR": atom["NMR"]
        }
