# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : C2addonCalculator.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import os
import shutil
import sys
import time

import dpdispatcher
import tqdm
from dpdispatcher import Machine, Resources, Task, Submission, dlog
from dpdispatcher.JobStatus import JobStatus
from fullerenedatapraser.io.recursion import recursion_files

dpdispatcher.dlog.handlers = [dpdispatcher.dlog.handlers[0]]

xtb_path = r"/home/hyb/anaconda3/envs/forxtb/bin/xtb"
# xtb_path = r"/root/anaconda3/envs/forxtb/bin/xtb"
local_root = "examplexyz/"

machine = Machine(batch_type="Slurm",
                  context_type="SSHContext",
                  local_root=local_root,
                  remote_root="/home/hyb/xtbcal/dispatcher/",
                  # remote_root="/root/xtbcal/dispatcher/",
                  remote_profile={
                      "hostname": "",
                      "username": "",
                      "password": "",
                      "port": 22,
                      "timeout": 10
                  },
                  )
resources = Resources(number_node=1,
                      cpu_per_node=4,
                      gpu_per_node=0,
                      group_size=10,
                      queue_name="N16")


def get_output_file_list(inputxtbname):
    outputfilelist = [
        "gradient",
        "charges",
        f"{inputxtbname}.engrad",
        "wbo",
        "xtbout.json",
        "xtbopt.log",
        "xtbopt.xyz"
    ]
    return outputfilelist


def get_output_file_store_list(inputxtbname):
    """
    Files name want to store in original directories.
    Must coupled with `get_output_file_list()`.

    """
    outputfilelist = [
        f"{inputxtbname}.gradient",
        f"{inputxtbname}.charges",
        f"{inputxtbname}.engrad",
        f"{inputxtbname}.wbo",
        f"{inputxtbname}.json",
        f"{inputxtbname}.log",
        f"{inputxtbname}.xyz"
    ]
    return outputfilelist


TASK_TABLE = r"task_finished.table"

SOURCE_ROOT = r"D:\CODE\#DATASETS\FullDB\C2addon"
from C2addonGenerator import lazy_mkdir

lazy_mkdir(SOURCE_ROOT)


def isomer_list(source_root, dirslice, spiral_slice=None):
    for dir_path in os.listdir(source_root):
        if int(dir_path.split("_")[0][1:]) in dirslice:
            if spiral_slice:
                if int(dir_path.split("_")[1][:9]) >= spiral_slice:
                    yield dir_path
            else:
                yield dir_path


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


if __name__ == '__main__':

    WORK_BASE = "xyzdispatchertest/"
    tbar = tqdm.tqdm(desc="Batch Working Start")
    for isomer in isomer_list(SOURCE_ROOT, range(56, 60, 2), 664):

        task_list = []

        tbar.set_description(f"Batch begin on {isomer[:-5]}")
        Source_dir = os.path.join(SOURCE_ROOT, isomer)
        for idx, item in enumerate(recursion_files(Source_dir, format="xyz", ignore_mode=True)):
            tbar.reset(total=len(os.listdir(Source_dir)))
            tbar.set_description(f"Batch Upload on {isomer[:-5]}")

            file_base_name = os.path.basename(item)
            file_name_without_ext = os.path.splitext(file_base_name)[0]
            input_file_path = os.path.join(local_root, WORK_BASE, str(idx), file_base_name)
            if not os.path.exists(input_file_path):
                try:
                    os.mkdir(os.path.join(local_root, WORK_BASE, str(idx)))
                except FileExistsError:
                    print("Not a clean `work_base`. Please Clean {}", file=sys.stderr)
                    exit(1)
                shutil.copy(item, input_file_path)
            test_TASK = Task(command=f"{xtb_path} {file_base_name} --opt tight --grad --json",
                             task_work_path=f"{idx}/",
                             forward_files=[file_base_name],
                             backward_files=get_output_file_list(file_name_without_ext)
                             )
            task_list.append(test_TASK)
            tbar.update()


        def tbar_update_server_status(jobstatus):
            tbar.reset(total=len(jobstatus))
            cont_unsubmitted = 0
            cont_waiting = 0
            cont_running = 0
            cont_terminated = 0
            cont_finished = 0
            cont_completing = 0
            cont_unknown = 0
            for stat in jobstatus:
                if stat == JobStatus.unsubmitted:
                    cont_unsubmitted += 1
                elif stat == JobStatus.waiting:
                    cont_waiting += 1
                elif stat == JobStatus.running:
                    cont_running += 1
                elif stat == JobStatus.terminated:
                    cont_terminated += 1
                elif stat == JobStatus.finished:
                    cont_finished += 1
                elif stat == JobStatus.completing:
                    cont_completing += 1
                else:
                    cont_unknown += 1
            tbar.update(cont_finished)
            tbar.set_postfix(Status=f"Total Job: {len(jobstatus)}, Finished: {cont_finished}, Running: {cont_running}, UnSub:{cont_unsubmitted}, Wait:{cont_waiting}, T:{cont_terminated}, CG:{cont_completing}",
                             )


        submission = InteractionSubmission(work_base=WORK_BASE,
                                           machine=machine,
                                           resources=resources,
                                           task_list=task_list,
                                           forward_common_files=[],
                                           backward_common_files=[]
                                           )
        submission.run_submission(call_back=tbar_update_server_status, check_time_interval=5)
        tbar.reset()
        tbar.set_postfix(Status="Running...")

        # working on calculated files
        for idx, item in enumerate(recursion_files(Source_dir, format="xyz", ignore_mode=True)):
            tbar.reset(total=len(os.listdir(Source_dir)))
            tbar.set_description(f"Batch Copy on {isomer[:-5]}")
            # copy files to origin directory.
            file_base_name = os.path.basename(item)
            file_name_without_ext = os.path.splitext(file_base_name)[0]
            task_work_path = os.path.join(local_root, WORK_BASE, str(idx))
            for outputfile, targetstorename in zip(get_output_file_list(file_name_without_ext), get_output_file_store_list(file_name_without_ext)):
                outputfile = os.path.join(task_work_path, outputfile)
                targetstorename = os.path.join(Source_dir, targetstorename)
                shutil.move(outputfile, targetstorename)
            shutil.rmtree(task_work_path)
            tbar.update()
        TASK_TABLE_FILE = open(TASK_TABLE, "a")
        print(isomer, file=TASK_TABLE_FILE)
        TASK_TABLE_FILE.close()

    tbar.close()
