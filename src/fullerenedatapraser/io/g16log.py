# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : g16log.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import os
import re

import numpy as np
from ase.atoms import Atoms
from fullerenedatapraser.util.functools import lazy_property
from fullerenedatapraser.util.logger import Logger

logger = Logger(__name__, console_on=True)


class LogFile(object):
    """The interface to the .log from Gaussian Program.

    LogFile object is the .log files and with its information in.
    Where there should be the content of each steps.

    Attributes
    ----------
        path(str): The path of the .log file.
        content(dict): The main information in .log file. And arranged by the file content.

    """
    # Six re compiled modules:

    par_tasktitle = re.compile(
        r' Leave Link    1 .*?\n \(Enter .*?.exe.*?--------------------\n (.*?)\n --------------------', re.S)  # TODO(yanbohan98@gmail.com): To completed.
    par_taskmethod = re.compile(
        r' #(.*?)\n', re.S)
    par_cputime = re.compile(
        r'Job cpu time:(.*?) days (.*?) hours (.*?) minutes (.*?) seconds.\n', re.S)
    par_NormalTerminate = re.compile(r'Normal termination', re.S)
    par_EnergyDictSCF = re.compile(r'SCF Done:.*?=  (.*?)     A.U.', re.S)
    par_StructureDictSCF = re.compile(
        r'                          Input orientation:                          \n ---------------------------------------------------------------------\n Center     Atomic      Atomic             Coordinates \(Angstroms\)\n Number     Number       Type             X           Y           Z\n ---------------------------------------------------------------------\n (.*?)\n ---------------------------------------------------------------------',
        re.S)
    par_bond = re.compile(r" R\((.*?)\)", re.S)

    # TODO(yanbaohan98@gmail.com): par compile molds should be created for GAP information and more other.

    def __init__(self, path):
        self.path = path
        # redundant information dict to Log files
        self.content = {'taskTitle': '',
                        'taskMethod': '',
                        "Atom_bond": [],
                        'StructureDict': [],
                        'CPUTime': None,
                        'NormalTerminate': False,
                        'EnergyDict': [],
                        'GAPDict': {
                            'SCFAttr': [],
                            'SCFEnergy': []
                        }
                        }
        # load the information from result .log file.
        self.__load()

    def __load(self, flag=None):
        """Console to Load the info from LOG files [path]

        """
        if self.path is not None:
            logger.info("Reading the LOG File from %s ." % self.path)

            self.__readfilesfromlogfile()

            logger.info("Reading the LOG File from %s progress Terminated." % self.path)

    def __readfilesfromlogfile(self):
        """The identity function.

        """
        with open(self.path) as file:
            information = file.read()
            # self.content['taskTitle'] = LogFile.par_tasktitle.findall(information)[0]
            self.content['taskTitle'] = os.path.basename(self.path)
            self.content['taskMethod'] = LogFile.par_taskmethod.findall(information)[0]
            try:
                self.content['CPUTime'] = [float(i) for i in LogFile.par_cputime.findall(information)[0]]
                self.content['NormalTerminate'] = (LogFile.par_NormalTerminate.findall(information)[0]) != ''
            except IndexError:
                # TODO(yanbohan98@gmail.com): TO Warning the failure to read the CPUTime and the Terminate cause.
                logger.warning(f"Job in file {self.path} is not normal terminated. Infomation may be unreliable.")
            self.content['EnergyDict'] = [float(i) for i in LogFile.par_EnergyDictSCF.findall(information)]
            self.content['StructureDict'] = [i for i in LogFile.par_StructureDictSCF.findall(information)][:-1]
            # The last Structure is the same to the second last one, which is the converged.
            Atom_bond_str = [i for i in LogFile.par_bond.findall(information)]
            Atom_bond_list = []
            for item in Atom_bond_str:
                Atom_bond_list.append(list(int(i) for i in item.split(',')))
            self.content['Atom_bond'] = Atom_bond_list
            logger.info("Successfully Read the File %s. Information has been Loaded." % self.path)

    @lazy_property
    def atoms(self):
        structurestr = self.content["StructureDict"]
        energy_list = self.content["EnergyDict"]
        if "freq" in "".join(self.content["taskMethod"]):
            structurestr.pop(-1)
            # Pop last output due to final freq task.
        # TODO: check more log files.
        atoms = []
        for molidx, molstr in enumerate(structurestr):
            molstr = molstr.split("\n")
            atom_num = len(molstr)
            numbers = np.zeros(atom_num, dtype=int)
            pos = np.zeros([atom_num, 3])
            for idx, atom in enumerate(molstr):
                atomitem = atom.split()
                numbers[idx] = int(atomitem[1])
                pos[idx] = np.array([float(x) for x in atomitem[-3:]])
            mol = Atoms(numbers=numbers, positions=pos, info={"energy": energy_list[molidx]})
            # TODO: Add charge read logical.
            atoms.append(mol)
        return atoms

    def log_to_file(self, target):
        """
        Export the content to a file as unicode.
        """
        with open(target, 'a') as file:
            file.write(str(self.content))
            logger.info("Information has been Loaded in {}".format(target))

    def brief_content(self):  #
        """
        Return a brief info of final energy and whether normal terminated.
        """
        # 输出最终收敛能量和计算情况（是否正常终止）
        return self.content['taskTitle'] + "\t" + self.content['taskMethod'] + "\t" + str(
            self.content['EnergyDict'][-1]) + '\t' + str(self.content['NormalTerminate']) + '\n'


def read_g16log_atoms(filepath):
    f = LogFile(filepath)
    return f.atoms
