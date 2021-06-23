#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.tools import LogCsv, SPath
import pandas

"""class LogCsv:
    def __init__(self, csv: SPath):
        self.csv = csv

    def __str__(self):
        return str(self.csv)

    @property
    def path(self):
        return self.csv

    @property
    def data(self):
        return self.eval()

    def eval(self, **kwargs):
        return pandas.read_csv(self.csv, **kwargs)

    def apply(self, new_data, **kwargs):
        return new_data.to_csv(self.csv, **kwargs)

    @staticmethod
    def _update(tmp_dat, org_lb, org_val, new_lb=None, new_val=None):
        if new_lb is None:
            tmp_dat.loc[tmp_dat[org_lb] == org_val, org_lb] = new_val
        else:
            tmp_dat.loc[tmp_dat[org_lb] == org_val, new_lb] = new_val
        return tmp_dat

    def update_one(self, label, value, new_label=None, new_value=None, **kwargs):
        tmp = self.data.copy()
        tmp = self._update(tmp, label, value, new_label, new_value)
        self.apply(tmp, index=False, **kwargs)

    def update_many(self, label, value, new_values: dict, **kwargs):
        tmp = self.data.copy()
        for key, val in new_values.items():
            try:
                tmp = self._update(tmp, label, value, key, val)
            except:
                continue
        self.apply(tmp, **kwargs)

    def drop_one(self, label, value, **kwargs):
        tmp = self.data.copy()
        row_list = tmp.loc[tmp[label] == value].index.tolist()
        tmp.drop(row_list, inplace=True, **kwargs)
        self.apply(tmp)

    def insert_one(self, data: pandas.DataFrame, **kwargs):
        tmp = self.data.copy()
        tmp = tmp.append(data, ignore_index=True)
        self.apply(tmp, **kwargs)

    def contain(self, label, val):
        tmp = self.data.copy()
        return bool(tmp.loc[tmp[label] == val].index.tolist())

    def get(self, label, val):
        tmp = self.data.copy()
        return tmp.loc[tmp[label] == val]

    def touch(self, head: list, values: list, **kwargs):
        nov = len(values)
        tmp = dataframe_from_dict(
            dict(zip(head, values[0]))
        )
        for idx in range(1, nov):
            tmp = tmp.append(
                dataframe_from_dict(
                    dict(zip(head, values[idx]))), ignore_index=True
            )
        self.apply(new_data=tmp, **kwargs)
"""
if __name__ == '__main__':
    f = r".local/all_job.csv"
    x = LogCsv(SPath(f))
    k = {"JOBID": 987654, "PD": "R", "NAME": "test1.sh"}
    v = {"JOBID": 87654, "PD": "R", "NAME": "test2.sh"}
    z = {"JOBID": 3, "PD": "R", "NAME": "test3.sh"}
    n = x.add(z)
    x.apply()


