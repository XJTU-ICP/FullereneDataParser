# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : recursion.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import os
from fullerenedatapraser.util.logger import Logger
from fullerenedatapraser.io import FileNotMatchError

logger = Logger(__name__, console_on=True)


def recursion_files(rootpath, format="xyz", ignore_mode=False):
    """
    Recurse files in `rootpath` with match file format `format`.
    Parameters
    ----------
    rootpath: str or path-like
    format: str or None
        If `format` set to "" or None, all files will be returned.
        Warning: Format will match all files contain ".{format}",
        which means "xxx.xyz1234" will be matched also.
        # TODO: A better way to match file.
    ignore_mode:bool
        If ignore_mode, files doesn't match format will be ignored.

    Returns
    -------
    Generator of file path.
    """
    root_list = os.listdir(rootpath)
    for item in root_list:
        item_path = os.path.join(rootpath, item)
        if os.path.isdir(item_path):
            for sub_item_path in list(recursion_files(item_path, format, ignore_mode)):
                if os.path.isfile(sub_item_path):
                    yield sub_item_path
        elif os.path.isfile(item_path):
            if format:
                if f".{format}" in os.path.splitext(item)[-1]:
                    yield item_path
                else:
                    if not ignore_mode:
                        raise FileNotMatchError(
                            f"There is at least one file not '.{format}' file, "
                             "Please make sure your data is clean."
                            f"The file is at {item_path}"
                        )
                    else:
                        logger.info(
                            f"Ingnore Mode for recursion files is set to `on`, "
                            f"All file doesn't match the format {format} will be ignored."
                        )
            else:
                yield item_path
