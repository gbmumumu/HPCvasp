#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from monty import os
import pandas

import logging

from utils.spath import SPath
from utils.tools import retry, get_output, LogCsv, dataframe_from_dict

TH_LOCAL = SPath(r"./.local").absolute()
TH_LOCAL.mkdir(exist_ok=True)
YHQ_HEAD = "JOBID,PARTITION,NAME,USER,ST,TIME,NODE,NODELIST(REASON),WORKDIR".split(',')
YHI_HEAD = ["CLASS", "ALLOC", "IDLE", "DRAIN", "TOTAL"]
RUNNING_JOB_LOG = LogCsv(SPath(TH_LOCAL / "running_job.csv"))
HPC_LOG = LogCsv(SPath(TH_LOCAL / "hpc.csv"))
TEMP_FILE = SPath(TH_LOCAL / "tmp.txt")


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
    def running_job_log(self):
        return RUNNING_JOB_LOG

    @retry(max_retry=5, inter_time=5)
    def yhcancel(self):
        ok, _ = get_output(f"yhcancel {self.id}")
        if ok != 0:
            return ok, None
        self.running_job_log.drop_one(label="JOBID", value=self.id)
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
        for keyword in YHQ_HEAD:
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
        pass

    @retry(max_retry=5, inter_time=5)
    def yhcontrol_show_job(self):
        ok, output = get_output(f"yhcontrol show job {self.id}")
        if ok != 0:
            return ok, None
        # output = SPath(r"C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\.local/yhcontrol.txt").read_text()
        _, update_data = self._yhcontrol_parser(output)
        job_id = update_data["JOBID"]
        try:
            if not self.running_job_log.is_contain("JOBID", job_id):
                new_data = dataframe_from_dict(update_data)
                self.running_job_log.insert_one(new_data, index=False)
            else:
                self.running_job_log.update_many("JOBID", job_id, update_data, index=False)
        except:
            return 1, None
        else:
            return 0, update_data


class TianHeWorker:
    def __init__(self, partition="work", total_allowed_node=50,
                 used_node=1, idle_node=None):
        self.partition = partition
        self.alloc = total_allowed_node
        self.used = used_node
        self.idle = idle_node

    @property
    def hpc_log(self):
        return HPC_LOG

    @property
    def running_job_log(self):
        return RUNNING_JOB_LOG

    @staticmethod
    def _yhi_parser(log: SPath):
        log = SPath(r"C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\.local/yhi.txt")
        if not log.is_empty():
            dat = log.read_text().split()
            for item in dat:
                if "/" in item:
                    try:
                        node_info = [int(i) for i in item.split("/")]
                    except:
                        break
                    else:
                        node_info.insert(0, "SLURM")
                        return 0, dataframe_from_dict(
                            dict(zip(YHI_HEAD,
                                     node_info))
                        )
        return 1, None

    @staticmethod
    def _yhq_parser(log: SPath):
        log = SPath(r"C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\.local/yhq.txt")
        if not log.is_empty():
            dat = pandas.read_table(log, sep=r"\s+")
            dat["WORKDIR"] = None
            return 0, dat
        return 1, None

    @retry(max_retry=5, inter_time=5)
    def yhq(self):
        #ok, _ = get_output(f"yhqueue | grep {self.partition} > {TEMP_FILE}")
        #if ok != 0:
        #    return ok, None
        ok, yhq_data = self._yhq_parser(TEMP_FILE)
        # TEMP_FILE.rm_file()
        if ok != 0:
            return ok, None
        return 0, yhq_data

    @retry(max_retry=5, inter_time=5)
    def yhi(self):
        #ok, _ = get_output(f"yhinfo -s | grep {self.partition} > {TEMP_FILE}")
        #if ok != 0:
        #    return ok, None
        ok, yhi_data = self._yhi_parser(TEMP_FILE)
        # TEMP_FILE.rm_file()
        if ok != 0:
            return ok, None

        return 0, yhi_data

    def flush(self):
        _, sys_yhi = self.yhi()
        _, user_yhq = self.yhq()
        self.used = user_yhq["NODES"].sum()
        user_yhi = dataframe_from_dict(
            dict(zip(YHI_HEAD,
                     ["User", self.alloc, self.used, None, None]))
        )
        sys_yhi.append(user_yhi, ignore_index=True)
        user_yhq.to_csv(str(self.running_job_log), index=False)
        print(sys_yhi)
        #yhi_data.to_csv(str(self.hpc_log), index=False)
        #print(used_node)

class TianHeNodes:
    def __init__(self, job_id, cn_list):
        self.job_id = job_id
        self.cn_list = cn_list

    @staticmethod
    def _string_parser(cn_string):
        tmp = cn_string.strip("[").strip("]")
        _tmp = tmp.split(',')
        used_nodes = []
        for i in _tmp:
            j = i.replace("cn[", "").replace("]", "")
            if '-' in j:
                s, e = j.split('-')
                used_nodes.extend(
                    [k for k in range(int(s), int(e) + 1)]
                )
            else:
                used_nodes.append(j)
        return used_nodes

    @property
    def running_job_log(self):
        return RUNNING_JOB_LOG

    @classmethod
    def from_log(cls, log: LogCsv):
        pass


if __name__ == "__main__":
    pass
