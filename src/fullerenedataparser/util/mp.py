# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : mp.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from fullerenedataparser.util.logger import Logger

logger = Logger(__name__, console_on=True)


def print_error(value):
    logger.error(f"Wrong when using process pool: {value}")
