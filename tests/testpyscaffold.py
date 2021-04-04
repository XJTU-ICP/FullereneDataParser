# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : testpyscaffold.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from pyscaffold.shell import *
from pyscaffold import file_system

content = "This is the original text."

with file_system.tmpfile(prefix="pyscaffold-", suffix=".args.sh") as file:
    file.write_text(content, "utf-8")
    content = edit(file).read_text("utf-8")
print(content)
