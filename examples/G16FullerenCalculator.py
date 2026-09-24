# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : G16FullerenCalculator.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #


import os
import shutil
import sys
import time

import ase.visualize
import dpdata
import dpdispatcher
import tqdm
from dpdispatcher import Machine, Resources, Task, Submission, dlog
from dpdispatcher.JobStatus import JobStatus
from fullerenedataparser.io.recursion import recursion_files
from ase.atoms import Atoms
from ase.io.gaussian import write_gaussian_in


class InteractionSubmission(Submission):
    def check_all_finished(self, call_back=None):
        self.get_submission_state()
        if call_back:
            call_back([job.job_state for job in self.belonging_jobs])
        if any((job.job_state in [JobStatus.terminated, JobStatus.unknown]) for job in self.belonging_jobs):
            self.submission_to_json()
        if any((job.job_state in [JobStatus.running,
                                  JobStatus.waiting,
                                  JobStatus.unsubmitted,
                                  JobStatus.completing,
                                  JobStatus.terminated,
                                  JobStatus.unknown]) for job in self.belonging_jobs):
            return False
        else:
            return True

    def run_submission(self, *, exit_on_submit=False, clean=True, call_back=None, check_time_interval=40):
        """main method to execute the submission.
        First, check whether old Submission exists on the remote machine, and try to recover from it.
        Second, upload the local files to the remote machine where the tasks to be executed.
        Third, run the submission defined previously.
        Forth, wait until the tasks in the submission finished and download the result file to local directory.
        if exit_on_submit is True, submission will exit.
        """
        if not self.belonging_jobs:
            self.generate_jobs()
        self.try_recover_from_json()
        if self.check_all_finished():
            dlog.info('info:check_all_finished: True')
        else:
            dlog.info('info:check_all_finished: False')
            self.upload_jobs()
            self.handle_unexpected_submission_state()
            self.submission_to_json()
        time.sleep(1)
        while not self.check_all_finished(call_back=call_back):
            if exit_on_submit is True:
                print('<<<<<<dpdispatcher<<<<<<SuccessSubmit<<<<<<exit 0<<<<<<')
                print(f"submission succeeded: {self.submission_hash}")
                print(f"at {self.machine.context.remote_root}")
                print("exit_on_submit")
                print('>>>>>>dpdispatcher>>>>>>SuccessSubmit>>>>>>exit 0>>>>>>')
                return self.serialize()
            try:
                time.sleep(check_time_interval)
            except KeyboardInterrupt as e:
                self.submission_to_json()
                print('<<<<<<dpdispatcher<<<<<<KeyboardInterrupt<<<<<<exit 1<<<<<<')
                print('submission: ', self.submission_hash)
                print(self.serialize())
                print('>>>>>>dpdispatcher>>>>>>KeyboardInterrupt>>>>>>exit 1>>>>>>')
                exit(1)
            except SystemExit as e:
                self.submission_to_json()
                print('<<<<<<dpdispatcher<<<<<<SystemExit<<<<<<exit 2<<<<<<')
                print('submission: ', self.submission_hash)
                print(self.serialize())
                print('>>>>>>dpdispatcher>>>>>>SystemExit>>>>>>exit 2>>>>>>')
                exit(2)
            except Exception as e:
                self.submission_to_json()
                print('<<<<<<dpdispatcher<<<<<<{e}<<<<<<exit 3<<<<<<'.format(e=e))
                print('submission: ', self.submission_hash)
                print(self.serialize())
                print('>>>>>>dpdispatcher>>>>>>{e}>>>>>>exit 3>>>>>>'.format(e=e))
                exit(3)
            else:
                self.handle_unexpected_submission_state()
            finally:
                pass
        self.handle_unexpected_submission_state()
        self.submission_to_json()
        self.download_jobs()
        if clean:
            self.clean_jobs()
        return self.serialize()


# xtb_path = r"/home/hyb/anaconda3/envs/forxtb/bin/xtb"
# # xtb_path = r"/root/anaconda3/envs/forxtb/bin/xtb"
TASK_TABLE = r"task_finished_G16.table"
from C2addonGenerator import lazy_mkdir

SOURCE_ROOT = r"D:\#Research\#projects\#DPTrain\xtbopt_fuller"
TARGET_DIR = r"D:\CODE\#DATASETS\FullDB\G16CalculatedFullerene"
lazy_mkdir(TARGET_DIR)
local_root = TARGET_DIR

machine = Machine(batch_type="Slurm",
                  context_type="SSHContext",
                  local_root=local_root,
                  remote_root="/home/hyb/g16cal/dispatcher/",
                  # remote_root="/root/xtbcal/dispatcher/",
                  remote_profile={
                      "hostname": "58.206.101.13",
                      "username": "hyb",
                      "password": "980417",
                      "port": 30022,
                      "timeout": 10
                  },
                  )
resources = Resources(number_node=1,
                      cpu_per_node=16,
                      gpu_per_node=0,
                      group_size=1,
                      queue_name="N16")


def batch_dpdata_trans(SOURCE_ROOT):
    task_list = []
    for direct in os.listdir(SOURCE_ROOT):
        direct = os.path.abspath(os.path.join(SOURCE_ROOT, direct))
        ms = dpdata.MultiSystems.from_dir(direct, "", fmt="deepmd/raw", recursive=False, Labeled=False)
        for sys in ms.systems.values():
            sys: dpdata.System
            sysname = sys.formula
            for idx, frame in enumerate(sys):
                frame: dpdata.System
                atom_names = frame.get_atom_names()
                atom_types = frame.get_atom_types()
                symbols = list([atom_names[atom_type] for atom_type in atom_types])
                coords = frame.data["coords"][0]
                tmp_atoms = Atoms(symbols=symbols, positions=coords)
                target_path = os.path.join(TARGET_DIR, f"{sysname}_{idx:03}.gjf")
                trans_dpdata_dir(tmp_atoms, target_path, f"{sysname}_{idx:03}")
                tmp_task = Task(command=f"g16 <{sysname}_{idx:03}.gjf >{sysname}_{idx:03}.log",
                                task_work_path=".",
                                forward_files=[f"{sysname}_{idx:03}.gjf"],
                                backward_files=[f"{sysname}_{idx:03}.log", f"{sysname}_{idx:03}.chk"]

                                )
                task_list.append(tmp_task)
    submission = InteractionSubmission(work_base=".",
                                       machine=machine,
                                       resources=resources,
                                       task_list=task_list,
                                       forward_common_files=[],
                                       backward_common_files=[]
                                       )
    submission.run_submission(check_time_interval=40)


def trans_dpdata_dir(atoms, target_path, task_name):
    with open(target_path, "w") as f:
        write_gaussian_in(
            f, atoms, method="opt b3lyp", basis="6-31G(d)",
            charge=0, mult=1, nprocshared=16, chk=task_name + ".chk",

        )


def make_gaussian_input(atoms, target_path):
    pass


if __name__ == '__main__':
    batch_dpdata_trans(SOURCE_ROOT)
