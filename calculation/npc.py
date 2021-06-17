#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from time import sleep
from multiprocessing.pool import Pool

from utils.yhurm import TianHeWorker, TianHeJob, TH_LOCAL
from utils.spath import SPath
from utils.tools import LogCsv
from calculation.vasp.workflow import WorkflowParser
from config import WORKFLOW, CONDOR

ALL_JOB_LOG = LogCsv(SPath(TH_LOCAL / "all_job.csv"))
_ALL_JOB_HEAD = ["JOBID", "ST", "WORKDIR", "NAME", "RESULT"]


class Producer(threading.Thread):
    def __init__(self, queue, worker: TianHeWorker, ):
        super(Producer, self).__init__()
        self.worker = worker
        self.queue = queue

    def run(self):
        if not ALL_JOB_LOG.path.exists():
            raise Exception("available job not found!")

        self.worker.flush()
        max_needed_node, max_needed_core = 0, 0
        for _, val in WORKFLOW.items():
            if max_needed_node < val["node"]:
                max_needed_node = val["node"]
            if max_needed_core < val["core"]:
                max_needed_core = val["core"]

        for index, job in ALL_JOB_LOG.data.iterrows():
            dft_job = TianHeJob(job_stat=job["RESULT"], job_path=job["WORKDIR"],
                                partition=CONDOR.get("ALLOW", "PARTITION"),
                                node=max_needed_node, core=max_needed_core, name=job["NAME"])
            self.queue.put(dft_job)
        print(self.queue.qsize())


class Submitter(threading.Thread):
    def __init__(self, queue, worker: TianHeWorker, stime=0.5):
        super(Submitter, self).__init__()
        self.queue = queue
        self.worker = worker
        self.stime = stime

    def run(self):
        while not self.queue.empty() and \
                self.worker.idle_node > 0 and \
                self.worker.used_node <= CONDOR.getint("ALLOW", "TOTAL_NODE"):
            job = self.queue.get()
            success, info = job.yhbatch()
            if success:
                info.update({"ST": "SS"})
                self.worker.idle_node -= job.node
                self.worker.used_node += job.node
            else:
                info.update({"ST": "SF"})
            ALL_JOB_LOG.update_many("WORKDIR", job.path, info)
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
            ALL_JOB_LOG.touch(_ALL_JOB_HEAD, jobs)
        except (AttributeError, IndexError):
            raise Exception("Job initialization failed !, check structure files or match pattern!")

        return True

    def post_process(self):
        pass


if __name__ == '__main__':
    pass
