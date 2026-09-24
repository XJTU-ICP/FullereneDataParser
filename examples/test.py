# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : test.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import os.path
import pathlib

DEFINE_CONT=1

def readG16Log(filename):
    res = {
        "filename": filename,
        "line": "",
        "success": False
    }
    with open(filename, "r") as f:
        for line in f.readlines():
            if line.startswith(" #"):
                res["line"] = line.split()
            if line.startswith(" Normal termination"):
                res["success"] = True
    return res


class G16File:
    def __init__(self, filename=None):
        self.filename = filename

    def __str__(self):
        return f"{self.filename} is here"

    def getFilename(self):
        return self.filename

    def readG16Log(self):
        res = {
            "filename": self.filename,
            "line": "",
            "success": False
        }
        with open(self.filename, "r") as f:
            for line in f.readlines():
                if line.startswith(" #"):
                    res["line"] = self.getCommand(line)
                if line.startswith(" Normal termination"):
                    res["success"] = True
        return

    def getCommand(self, line):
        return line.split()

    def getNormalTermination(self):
        pass

    def getxyz(self):
        pass



if __name__ == '__main__':
    f = r"C:\Users\hanyanbo98\PycharmProjects\FullereneDataPraser\tests\files\logfiles"
    filelist = pathlib.Path(f).iterdir()
    for filename in filelist:
        if filename.as_posix().endswith(".log"):
            print(G16File(filename=filename).readG16Log())
