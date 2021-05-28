#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas

from monty import os

from utils.spath import SPath
from utils.tools import retry, get_output, LogCsv

TH_LOCAL = SPath(r"./.local").absolute()
TH_LOCAL.mkdir(exist_ok=True)


class THCommandFailed(Exception):
    pass


class TianHeJob:
    def __init__(self, job_id=None, job_path=None, job_stat=None,
                 node=1, core=24, partition="work", script_filename=None):
        self.id = job_id
        self.path = job_path
        self.stat = job_stat
        self.node = node
        self.core = core
        self.partition = partition
        self.sfn = script_filename

    @property
    def job_log(self):
        return LogCsv(SPath(TH_LOCAL/"job.csv"))

    @retry(max_retry=5, inter_time=5)
    def yhcancel(self):
        ok, _ = get_output(f"yhcancel {self.id}")
        if ok:
            self.job_log.drop_one(label="JOBID", value=self.id)
            return True

        return False

    @staticmethod
    def _yhcancel_parser(output):
        pass

    @staticmethod
    def _yhbatch_parser(output):
        pass

    @staticmethod
    def _yhcontrol_parser(output):
        pass

    @retry(max_retry=5, inter_time=5)
    def yhbatch(self):
        with os.cd(self.path):
            ok, output = get_output(f"yhbatch -p {self.partition} -N {self.node} -n {self.core} {self.sfn}")

    @retry(max_retry=5, inter_time=5)
    def yhrun(self):
        raise NotImplementedError

    @retry(max_retry=5, inter_time=5)
    def yhcontrol_show_job(self):
        pass


class TianHeWorker:
    def __init__(self, partition="work", total_allowed_node=50,
                 used_node=1, idle_node=None):
        self.partition = partition

    @staticmethod
    def _yhq_parser(log: SPath):
        if not log.is_empty():
            dat = pandas.read_table(log, sep=r"\s+")
            dat.to_csv(log)
            return 1,
        return 0,

    @staticmethod
    def _yhi_parser():
        pass

    @property
    def yhq_log(self):
        return SPath(f"{TH_LOCAL}/yhq.txt")

    @retry(max_retry=5, inter_time=5)
    def yhq(self):
        ok, _ = get_output(f"yhqueue | grep {self.partition} > {self.yhq_log}")

        if not ok:
            raise THCommandFailed

        return self._yhq_parser(self.yhq_log)

    @retry(max_retry=5, inter_time=5)
    def yhi(self):
        ok, _ = get_output(f"yhinfo -s | grep {self.partition}")
        if not ok:
            raise THCommandFailed

        return self._yhi_parser()


class TianHeCn:
    def __init__(self, cn_list):
        self.cn_list = cn_list

    @staticmethod
    def _cn_parser(cn_string):
        pass

    @classmethod
    def from_log(cls, log):
        pass


if __name__ == "__main__":
    pass
