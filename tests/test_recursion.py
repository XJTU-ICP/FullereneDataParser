import logging
import os

import pytest
from fullerenedatapraser.io import FileNotMatchError
from fullerenedatapraser.io.recursion import recursion_files
from fullerenedatapraser.util.config import SetModuleEnvValue

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"

TEST_PATH = os.path.abspath(__name__)

with SetModuleEnvValue("log_level", logging.WARNING):
    def test_recursion_with_format():
        """Recursion file Tests, using format constrain"""
        filelist = list(recursion_files(os.path.join(TEST_PATH, "files"), format="xyz", ignore_mode=True))
        # assert r"files\subdirectory\dummy" in filelist
        assert os.path.join(TEST_PATH, r"files\subdirectory\C28_000000001opt.xyz") in filelist
        assert os.path.join(TEST_PATH, r"files\C28_000000001opt.xyz") in filelist
        assert os.path.join(TEST_PATH, r"files\C28_000000001opted.xyz") in filelist

    def test_recursion_without_format():
        """Recursion file Tests, without format constrain"""
        filelist = list(recursion_files(os.path.join(TEST_PATH, "files"), format=None))
        assert os.path.join(TEST_PATH, r"files\subdirectory\dummy") in filelist
        assert os.path.join(TEST_PATH, r"files\subdirectory\C28_000000001opt.xyz") in filelist
        assert os.path.join(TEST_PATH, r"files\C28_000000001opt.xyz") in filelist
        assert os.path.join(TEST_PATH, r"files\C28_000000001opted.xyz") in filelist

    def test_recursion_exception_with_format():
        """Recursion file Tests, with format constrain and hope A FileNotMatchError could be raised."""
        with pytest.raises(FileNotMatchError):
            list(recursion_files(os.path.join(TEST_PATH, "files"), format="xyz", ignore_mode=False))
