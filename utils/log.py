#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path as osp
import pandas
from utils.tools import SPath, dataframe_from_dict

PROG_PATH = SPath(osp.abspath(__file__)).parent.parent
TH_LOCAL = PROG_PATH / ".local"
TH_LOCAL.mkdir(exist_ok=True)


class LogCsv:
    def __init__(self, csv: SPath):
        self._path = csv
        self._csv = None
        if self._path.exists():
            self._csv = pandas.read_csv(self._path, sep="\t")

    def __repr__(self):
        return str(self._path)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, new_csv):
        self._csv = new_csv

    @property
    def path(self):
        return self._path

    def __str__(self):
        return repr(self.csv)

    def apply_(self, df: pandas.DataFrame):
        return df.to_csv(self._path, sep="\t", na_rep="?", index=False)

    def apply(self):
        self.apply_(self.csv)

    def add(self, new_data):
        tmp = self.csv.copy()
        tmp = tmp.append(new_data, ignore_index=True)
        self.csv = tmp
        return tmp

    def alter(self, lb, old_val, new_val):
        tmp = self.csv.copy()
        tmp = self._alter(tmp, lb, old_val, new_val)
        self.csv = tmp
        return tmp

    def alter_(self, match_lb, match_val, alter_lb, alter_val):
        tmp = self.csv.copy()
        tmp = self.__alter(tmp, match_lb, match_val, alter_lb, alter_val)
        self.csv = tmp
        return tmp

    @staticmethod
    def _alter(df, mk, mv, nv):
        df.loc[df[mk] == mv, mk] = nv
        return df

    @staticmethod
    def __alter(df, mk, mv, ak, av):
        df.loc[df[mk] == mv, ak] = av
        return df

    def alter_many(self, match_lb, match_val, values):
        tmp = self.csv.copy()
        for k, v in values.items():
            tmp = self.__alter(tmp, match_lb, match_val, k, v)
        self.csv = tmp
        return tmp

    def drop_one(self, label, value, **kwargs):
        tmp = self.csv.copy()
        row_list = tmp.loc[tmp[label] == value].index.tolist()
        tmp = tmp.drop(row_list, inplace=True, **kwargs)
        self.csv = tmp
        return tmp

    def contain(self, label, val):
        tmp = self.csv.copy()
        return bool(tmp.loc[tmp[label] == val].index.tolist())

    def get(self, label, val):
        tmp = self.csv.copy()
        return tmp.loc[tmp[label] == val]

    def touch(self, head: list, values: list):
        nov = len(values)
        tmp = dataframe_from_dict(
            dict(zip(head, values[0]))
        )
        for idx in range(1, nov):
            tmp = tmp.append(
                dataframe_from_dict(
                    dict(zip(head, values[idx]))), ignore_index=True
            )
        self.apply_(tmp)


_YHQ_HEAD = ["JOBID", "PARTITION", "NAME", "USER", "ST", "TIME", "NODE", "NODELIST(REASON)"]
_YHI_HEAD = ["CLASS", "ALLOC", "IDLE", "DRAIN", "TOTAL"]
RUNNING_JOB_LOG = LogCsv(SPath(TH_LOCAL / "running_job.csv"))
HPC_LOG = LogCsv(SPath(TH_LOCAL / "hpc.csv"))
TEMP_FILE = SPath(TH_LOCAL / "tmp.txt")
ALL_JOB_LOG = LogCsv(SPath(TH_LOCAL / "all_job.csv"))
_ALL_JOB_HEAD = ["JOBID", "ST", "WORKDIR", "NAME", "RESULT"]
_ERROR_JOB_HEAD = ["JOB_PATH", "ERROR_CODE", "ERROR_NAME"]
ERROR_JOB_LOG = LogCsv(SPath(TH_LOCAL / "error_job.csv"))


class Notice:
    pass


if __name__ == '__main__':
    pass
