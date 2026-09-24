# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : multiprocess_learn.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import os
import random
import time
import sys
from functools import partial
from multiprocessing import Pool, RLock, freeze_support, Pipe
from threading import Thread

from tqdm import tqdm
from colorama import init, Fore, Back, Style

def _progress_bar(parent, total_len, desc):
    desc = desc if desc else "Main"
    pb_main = tqdm(total=total_len, desc=desc, position=0,leave=None)
    nums = 0
    while True:
        msg = parent.recv()[0]
        if msg is not None:
            pb_main.update()
            nums += 1
        if nums >= total_len:
            break
    pb_main.close()


def _apply_single(ds, _apply_field=None, func=None, pipe=None, desc=None, proc_id=None):
    desc = desc if desc else f"# {proc_id}: "
    results = []
    for idx, tqdmins in tqdm(enumerate(ds), total=len(ds), desc=desc,leave=None):
        if _apply_field is not None:
            results.append(func(tqdmins[_apply_field]))
        else:
            results.append(func(tqdmins))

        if pipe is not None:
            pipe.send([idx + 1])

    return results


def apply_on_subprocess(ds, proc_id=None):
    time.sleep(random.random())
    return {"ds": ds}


def err_(e):
    print(e)


if __name__ == '__main__':
    os.system('cls')
    sys.stdout = sys.__stdout__
    print(Fore.GREEN + 'Green text')
    to_be_iterate = [range(i) for i in [60, 60, 60, 60, 60, 60]]
    parent, child = Pipe()
    main_thread = Thread(target=_progress_bar, args=(parent, len(to_be_iterate)*60, "Main"))
    main_thread.start()
    pool = Pool(processes=2, initializer=tqdm.set_lock, initargs=(RLock(),))
    poolouts = []
    for idx, item in enumerate(to_be_iterate):
        poolouts.append(pool.apply_async(_apply_single, kwds={"func": apply_on_subprocess, "ds": item, "proc_id": idx, "pipe": child}, error_callback=err_))
    pool.close()
    pool.join()
    main_thread.join()
    print(list([i.get() for i in poolouts]))
