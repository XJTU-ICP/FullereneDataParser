# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : orbital_csi_discutoff.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import multiprocessing
import pathlib
import pickle
import re
import time
from multiprocessing import RLock, Pool
from threading import Thread

import numpy
import numpy as np
from tqdm import tqdm

from fullerenedataparser.io.xyz import simple_read_xyz_xtb

# Draw distance of fullerene cages.
XYZ_STORE_PREFIX = r"D:\CODE\#DATASETS\FullDB\xTBcal"
DIS_STORE_PREFIX = r"D:\CODE\#DATASETS\FullDB\distanceMat"
C_XX_pattern = re.compile("C.*[0-9]")


def distance_dump(xyzname):
    distance = {}
    tbarsub = tqdm(list(basename.iterdir()))
    for xyz in tbarsub:
        tbarsub.desc = f"Now {xyz.name}"
        f = simple_read_xyz_xtb(filepath=xyz.as_posix(), index=slice(-1))
        f = list(f)[-1]
        dis_mat: numpy.ndarray = f.get_all_distances()
        distance[xyz.name] = dis_mat[np.tril_indices(dis_mat.shape[0], -1)]


def err_(e):
    print(e)


def dump_distance(args):
    distance = args["distance"]
    basename = args["basename"]
    with open(pathlib.Path(DIS_STORE_PREFIX) / (basename.name + ".dis"), "wb") as file:
        pickle.dump(distance, file)


def task(position, lock, task_group, pipe=None):
    iterations = task_group
    total_iterations = iterations

    with lock:
        bar = tqdm(
            desc=f'{task_group}',
            total=total_iterations,
            position=position,
            leave=False
        )

    distance = {}
    for xyz in range(iterations):
        # f = simple_read_xyz_xtb(filepath=xyz.as_posix(), index=slice(-1))
        # f = list(f)[-1]
        # dis_mat: numpy.ndarray = f.get_all_distances()
        # distance[xyz.name] = dis_mat[np.tril_indices(dis_mat.shape[0], -1)]
        time.sleep(xyz / 1000)
        with lock:
            bar.update(1)
    # with open(pathlib.Path(DIS_STORE_PREFIX) / (task_group.name + ".dis"), "wb") as file:
    #     pickle.dump(distance, file)

    with lock:
        if pipe is not None:
            pipe.send([1])
        bar.close()

    return {
        "distance": distance,
        "basename": task_group.name
    }


def _progress_bar(parent, total_len, desc, progress_end, global_lock):
    desc = desc if desc else "Main"
    pb_main = tqdm(total=total_len, desc=desc, position=progress_end)
    nums = 0
    while True:
        msg = parent.recv()[0]
        if msg is not None:
            with global_lock:
                pb_main.update()
                nums += 1
        if nums >= total_len:
            break
    pb_main.close()


def get_aviable_show_position(show_situation, global_lock):
    with global_lock:
        for idx, item in show_situation:
            if item == 0:
                show_situation[idx] = 1
                return idx


def release_show_position(idx, show_situation, global_lock):
    with global_lock:
        show_situation[idx] = 0


if __name__ == '__main__':
    global_lock = multiprocessing.Manager().Lock()
    processor = 2
    show_situation = [0 for _ in range(processor)]
    parent, child = multiprocessing.Pipe()
    to_be_iterate = [19, 2, 5, 1, 6, 8]
    iterate_len = len(to_be_iterate)
    iterate_situation = [multiprocessing.Manager().Lock() for _ in range(iterate_len)]
    main_thread = Thread(target=_progress_bar, kwargs={"parent": parent,
                                                       "total_len": iterate_len,
                                                       "desc": "All data",
                                                       "progress_end": 0,
                                                       "global_lock": global_lock})
    main_thread.start()
    with Pool(processes=processor, initializer=tqdm.set_lock, initargs=(RLock(),)) as pool:
        for idx, position in enumerate(to_be_iterate):
            pool.apply_async(
                task,
                kwds={
                    "task_group": position,
                    "position": idx % processor + 1,
                    "lock": iterate_situation[idx],
                    "pipe": child
                },
                callback=dump_distance,
                error_callback=err_
            )
        pool.close()
        pool.join()
    main_thread.join()
