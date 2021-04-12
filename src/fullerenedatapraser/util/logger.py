# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : logger.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import logging

from fullerenedatapraser.util.config import getGlobValue

__all__ = [
    "InfoLogger", "Logger"
]

"""
Predefined Loggers for project.
Usage:
```
from ..util.logger import InfoLogger

logger = InfoLogger(__name__,...) # all log above Info level will be logged. 

```

"""


class BaseLogging(logging.Logger):
    def __init__(self, name, level=logging.INFO, file=None, console_on=False):
        """

        Parameters
        ----------
        name: str
            Name of logger
        level: int
            logging.INFO, logging.DEBUG,...
        file: str or None
            File name of log.
            If None, log to console.
        console_on: bool
            If console_on, log to console anyway.
        """
        super().__init__(name, level)

        # format set of log
        fmt = "PID:%(process)d [%(asctime)s]-[%(name)s]-[%(levelname)s]-[%(filename)s,line %(lineno)d] : %(message)s"
        formatter = logging.Formatter(fmt)

        # to file
        if file:
            file_handle = logging.FileHandler(file, encoding="utf-8")
            file_handle.setFormatter(formatter)
            self.addHandler(file_handle)
        # to console when not setting log file.
        else:
            console_handle = logging.StreamHandler()
            console_handle.setFormatter(formatter)
            self.addHandler(console_handle)

        # use console out when setting log file.
        if file:
            if console_on:
                console_handle = logging.StreamHandler()
                console_handle.setFormatter(formatter)
                self.addHandler(console_handle)


class InfoLogger(BaseLogging):
    """
    Default Logger to console with INFO level.
    Set file to a real file to log in file.
    Parameters
    ----------
    name: str
        Name of logger
    """

    def __init__(self, name, **kwargs):
        super(InfoLogger, self).__init__(name=name, level=logging.INFO, **kwargs)


class DebugLogger(BaseLogging):
    """
    Default Logger to console with DEBUG level.
    Set file to a real file to log in file.
    Parameters
    ----------
    name: str
        Name of logger
    """

    def __init__(self, name, **kwargs):
        super(DebugLogger, self).__init__(name=name, level=logging.DEBUG, **kwargs)


def getLogger(level=logging.DEBUG):
    """
    Generate a logger with level.
    Parameters
    ----------
    level

    Returns
    -------
    A BaseLogging class.
    """

    class RunTimeLogger(BaseLogging):
        def __init__(self, name, **kwargs):
            super(RunTimeLogger, self).__init__(name=name, level=level, **kwargs)

        def isEnabledFor(self, level: int) -> bool:
            self.setLevel(level=getGlobValue("log_level"))
            self.level=getGlobValue("log_level")
            return super(RunTimeLogger,self).isEnabledFor(level)


    return RunTimeLogger


Logger = getLogger(level=getGlobValue("log_level"))

# class WarningLogger(BaseLogging):
#     """
#     Default Logger to console with WARNING level.
#     Set file to a real file to log in file.
#     Parameters
#     ----------
#     name: str
#         Name of logger
#     """
#
#     def __init__(self, name, **kwargs):
#         super(WarningLogger, self).__init__(name=name, level=logging.WARNING, **kwargs)
#
#
# class ErrorLogger(BaseLogging):
#     """
#     Default Logger to console with ERROR level.
#     Set file to a real file to log in file.
#     Parameters
#     ----------
#     name: str
#         Name of logger
#     """
#
#     def __init__(self, name, **kwargs):
#         super(ErrorLogger, self).__init__(name=name, level=logging.ERROR, **kwargs)
#
#
# class CriticalLogger(BaseLogging):
#     """
#     Default Logger to console with CRITICAL level.
#     Set file to a real file to log in file.
#     Parameters
#     ----------
#     name: str
#         Name of logger
#     """
#
#     def __init__(self, name, **kwargs):
#         super(CriticalLogger, self).__init__(name=name, level=logging.CRITICAL, **kwargs)

# TODO: Delete Me.
# if __name__ == '__main__':
#     from fullerenedatapraser.util.config import setGlobValue
#
#     setGlobValue("log_level", logging.DEBUG)
#     # print(getGlobValue("log_level"))
#     Logger = getLogger(getGlobValue("log_level"))
#     logger = Logger(__name__, console_on=True)
#     print(logger.level)
#     logger.debug("Hi")
