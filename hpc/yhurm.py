#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from monty import os
import pandas

from utils.spath import SPath
from utils.tools import retry, get_output, LogCsv

TH_LOCAL = SPath(r"./.local").absolute()
TH_LOCAL.mkdir(exist_ok=True)
JOB_HEAD = "JOBID,PARTITION,NAME,USER,ST,TIME,NODE,NODELIST(REASON),WORKDIR".split(',')


class THCommandFailed(Exception):
    pass


class TianHeJob:
    def __init__(self, job_id=None, job_path=None, job_stat=None,
                 node=1, core=24, partition="work", name=None):
        self.id = job_id
        self.path = job_path
        self.stat = job_stat
        self.node = node
        self.core = core
        self.partition = partition
        self.name = name

    @property
    def job_log(self):
        return LogCsv(SPath(TH_LOCAL / "job.csv"))

    @retry(max_retry=5, inter_time=5)
    def yhcancel(self):
        ok, _ = get_output(f"yhcancel {self.id}")
        if ok != 0:
            return ok, None
        self.job_log.drop_one(label="JOBID", value=self.id)
        return 0, None

    @staticmethod
    def _yhbatch_parser(output, **kwargs):
        job_id = output.split()[-1]
        kwargs.update({"JOBID": job_id})
        return 0, kwargs

    @staticmethod
    def _yhcontrol_parser(output):
        regex = re.compile(r"\s*(.*?)=(.*?)\s+?")
        control = {}
        for keyword in JOB_HEAD:
            for key, val in regex.findall(output):
                key = key.upper()
                if keyword == key:
                    control.update({key: int(val) if val.isnumeric() else val})
                else:
                    if "NumNodes".upper() == key:
                        control.update({"NODE": int(val)})
                    if "Account".upper() == key:
                        control.update({"USER": val})
                    if "NodeList".upper() == key:
                        control.update({"NODELIST(REASON)": val})
                    if "RunTime".upper() == key:
                        control.update({"TIME": val})
                    if "JobState".upper() == key:
                        control.update({"ST": val})
        return 0, control

    @retry(max_retry=5, inter_time=5)
    def yhbatch(self):
        with os.cd(self.path):
            ok, output = get_output(f"yhbatch -p {self.partition} "
                                    f"-N {self.node} -n {self.core} {self.name}")
        if ok != 0:
            return ok, None
        return self._yhbatch_parser(output, **{"WORKDIR": self.path,
                                               "NAME": self.name})

    @retry(max_retry=5, inter_time=5)
    def yhrun(self):
        raise NotImplementedError

    @retry(max_retry=5, inter_time=5)
    def yhcontrol_show_job(self):
        #ok, output = get_output(f"yhcontrol show job {self.id}")
        #if ok != 0:
        #    return ok, None
        output = SPath(r"C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\.local/yhcontrol.txt").read_text()
        ok, update_data = self._yhcontrol_parser(output)
        job_id = update_data["JOBID"]
        try:
            if not self.job_log.is_contain("JOBID", job_id):
                tmp = {}
                for k, v in update_data.items():
                    tmp[k] = [v]
                new_data = pandas.DataFrame.from_dict(tmp)
                del tmp
                self.job_log.insert_one(new_data, index=False)
            else:
                self.job_log.update_many("JOBID", job_id, update_data, index=False)
        except:
            return 1, None
        else:
            return 0, update_data


class TianHeWorker:
    def __init__(self, partition="work", total_allowed_node=50,
                 used_node=1, idle_node=None):
        self.partition = partition

    @staticmethod
    def _yhq_parser(log: SPath):
        if not log.is_empty():
            dat = pandas.read_table(log, sep=r"\s+")
            dat.to_csv(log)
            return 0,
        return 1,

    @staticmethod
    def _yhi_parser():
        pass

    @property
    def yhq_log(self):
        return SPath(f"{TH_LOCAL}/yhq.txt")

    @retry(max_retry=5, inter_time=5)
    def yhq(self):
        ok, _ = get_output(f"yhqueue | grep {self.partition} > {self.yhq_log}")

        if ok != 0:
            raise THCommandFailed

        return self._yhq_parser(self.yhq_log)

    @retry(max_retry=5, inter_time=5)
    def yhi(self):
        ok, _ = get_output(f"yhinfo -s | grep {self.partition}")
        if ok != 0:
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
