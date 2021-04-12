import pytest

# Inmport Some packages
from fullerenedatapraser.util.config import GlobalVar, setGlobValue, getGlobValue, SetModuleEnvValue
import logging

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"


@pytest.fixture(scope="function", autouse=True)
def test_Global_var_constant():
    assert getGlobValue("varfortest") is None
    assert getGlobValue("log_level") == logging.WARNING


@pytest.mark.usefixtures("test_Global_var_constant")
def test_set_Global_Value():
    assert getGlobValue("varfortest") is None
    setGlobValue("varfortest", 1)
    assert getGlobValue("varfortest") == 1
    delattr(GlobalVar, "varfortest")
    assert getGlobValue("varfortest") is None


@pytest.mark.usefixtures("test_Global_var_constant")
def test_set_Module_Env_Value():
    assert getGlobValue("log_level") is logging.WARNING
    with SetModuleEnvValue("log_level", logging.ERROR):
        assert getGlobValue("log_level") == logging.ERROR
    assert getGlobValue("log_level") is logging.WARNING
    assert getGlobValue("varfortest") is None
    with SetModuleEnvValue("varfortest", 1):
        assert getGlobValue("varfortest") == 1
    assert getGlobValue("varfortest") is None
    assert hasattr(GlobalVar, "varfortest") is False
