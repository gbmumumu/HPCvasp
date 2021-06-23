#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from time import sleep
from multiprocessing.pool import Pool

from utils.yhurm import TianHeWorker, TianHeJob
from utils.spath import SPath
from utils.log import ALL_JOB_LOG, ALL_JOB_LABEL
from calculation.vasp.workflow import WorkflowParser
from config import WORKFLOW, CONDOR


class Producer(threading.Thread):
    Finished = True

    def __init__(self, queue):
        super(Producer, self).__init__()
        self.queue = queue

    def run(self):
        if not ALL_JOB_LOG.path.exists():
            raise Exception("available job not found!")

        max_needed_node, max_needed_core = 0, 0
        for _, val in WORKFLOW.items():
            if max_needed_node < val["node"]:
                max_needed_node = val["node"]
            if max_needed_core < val["core"]:
                max_needed_core = val["core"]
        if ALL_JOB_LOG.csv is None:
            raise FileNotFoundError("No structure files found!")
             
        for index, job in ALL_JOB_LOG.csv.iterrows():
            dft_job = TianHeJob(job_stat=job["RESULT"], job_path=job["WORKDIR"],
                                partition=CONDOR.get("ALLOW", "PARTITION"),
                                node=max_needed_node, core=max_needed_core, name=job["NAME"])
            self.queue.put(dft_job)
        self.queue.put(self.Finished)


class Submitter(threading.Thread):
    Finished = True

    def __init__(self, queue, worker: TianHeWorker, stime=0.5, flush_time=60):
        super(Submitter, self).__init__()
        self.queue = queue
        self.worker = worker
        self.stime = stime
        self.ftime = flush_time

    def run(self):
        allow_node = CONDOR.getint("ALLOW", "TOTAL_NODE")
        while True:
            job = self.queue.get()
            if job is self.Finished:
                break
            print("Idle node: ", self.worker.idle_node)
            print("Used node: ", self.worker.used_node)
            while self.worker.idle_node <= 0 or self.worker.used_node >= allow_node:
                sleep(self.ftime)
                self.worker.flush()
            success, info = job.yhbatch()
            print(success, info)
            if success:
                info.update({"ST": "SS"})
                self.worker.idle_node -= job.node
                self.worker.used_node += job.node
            else:
                info.update({"ST": "SF"})
            ALL_JOB_LOG.alter_many("WORKDIR", job.path, info)
            ALL_JOB_LOG.apply()
            sleep(self.stime)


class Npc:
    def __init__(self, structures_path: SPath, interval_time=0.5):
        self.structures_path = structures_path
        self.interval_time = interval_time

    @staticmethod
    def _init(name: SPath, *args, **kwargs):
        filename_dir = name.mkdir_filename()
        name.copy_to(filename_dir, mv_org=True)
        return WorkflowParser(work_root=filename_dir, *args, **kwargs).write_sh()

    def init_jobs(self, pat, n=4):
        job_pool = Pool(n)
        job_dirs = []
        for structure in self.structures_path.walk(pattern=pat, is_file=True):
            job = job_pool.apply_async(self._init, args=(structure,))
            job_dirs.append(job)

        job_pool.close()
        job_pool.join()
        jobs = []
        for job in job_dirs:
            root, bash_name = job.get()
            jobs.append(["", "PD", root, bash_name, ""])

        try:
            ALL_JOB_LOG.touch(ALL_JOB_LABEL, jobs)
        except (AttributeError, IndexError):
            raise Exception("Job initialization failed !, check structure files or match pattern!")

        return True

    def post_process(self):
        pass


if __name__ == '__main__':
    pass
