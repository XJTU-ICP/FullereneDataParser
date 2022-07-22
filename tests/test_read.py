import os

import pytest
from fullerenedataparser.io import FileCommentError
from fullerenedataparser.io.g16log import read_g16log_atoms, LogFile
from fullerenedataparser.io.xyz import simple_read_xyz_xtb

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"

TEST_PATH = os.path.dirname(__file__)

def test_read_xyz():
    """xyz read one Tests"""
    f = os.path.join(TEST_PATH, r"files/C28_000000001opted.xyz")
    atomlist = simple_read_xyz_xtb(f, read_comment=False)
    assert len(list(atomlist)) == 1


def test_read_xyz_read_comment():
    """xyz read one Tests with comment"""
    f = os.path.join(TEST_PATH, r"files/C28_000000001opted.xyz")
    atomlist = list(simple_read_xyz_xtb(f, read_comment=True))
    assert len(atomlist) == 1
    assert len(atomlist[0].info) == 0


def test_read_xyz_read_unformat_comment():
    """xyz read one Tests"""
    f = os.path.join(TEST_PATH, r"files/OtherComment.xyz")
    with pytest.raises(FileCommentError):
        atomlist = list(simple_read_xyz_xtb(f, read_comment=True))


def test_read_xyzs():
    """xyz read multiple Tests"""
    f = os.path.join(TEST_PATH, r"files/C28_000000001opt.xyz")
    atomlist = simple_read_xyz_xtb(f)
    assert len(list(atomlist)) == 10


def test_xyz_values():
    f = os.path.join(TEST_PATH, r"files/C28_000000001opt.xyz")
    atomlist = simple_read_xyz_xtb(f)
    atoms = list(atomlist)[-1]
    assert atoms.info["energy"] == -59.368405988605


def test_log_read():
    f = os.path.join(TEST_PATH, r"files/logfiles/C20_Ih_1.log")
    atoms = read_g16log_atoms(f)
    assert len(atoms) == 15
    f = os.path.join(TEST_PATH, r"files/logfiles/C24_D6d_1.log")
    atoms = read_g16log_atoms(f)
    assert len(atoms) == 35


# TODO: check more log files.

def test_log_brief_read():
    f = os.path.join(TEST_PATH, r"files/logfiles/C24_D6d_1.log")
    atoms = LogFile(f)
    assert atoms.brief_content() == "C24_D6d_1.log	 opt freq b3lyp/6-31G(d,p) empiricaldispersion=gd3	-913.874862231	True\n"
