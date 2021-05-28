#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getstatusoutput
from time import sleep
import pandas

from utils.spath import SPath


def retry(max_retry=None, inter_time=None):
    if max_retry is None:
        max_retry = 3
    if inter_time is None:
        inter_time = 2

    def decorator(func):
        def inner(*args, **kwargs):
            exit_code, results = func(*args, **kwargs)
            number = 0
            if exit_code != 0:
                while number < max_retry:
                    sleep(inter_time)
                    number += 1
                    print(f'{number} times')
                    exit_code, results = func(*args, **kwargs)
                    if exit_code == 0:
                        break
            return exit_code, results

        return inner

    return decorator


def dataframe_from_dict(data: dict):
    tmp = {}
    for k, v in data.items():
        tmp[k] = [v]
    new_data = pandas.DataFrame.from_dict(tmp)
    del tmp
    return new_data


def get_output(unix_cmd):
    return getstatusoutput(unix_cmd)


class LogCsv:
    def __init__(self, csv: SPath):
        self.csv = csv

    def __str__(self):
        return str(self.csv)

    @property
    def data(self):
        return self.eval()

    def eval(self, **kwargs):
        return pandas.read_csv(self.csv, **kwargs)

    def apply(self, new_data, **kwargs):
        return new_data.to_csv(self.csv, **kwargs)

    @staticmethod
    def _update(tmp_dat, org_lb, org_val, new_label=None, new_val=None):
        if new_label is None:
            tmp_dat.loc[tmp_dat[org_lb] == org_val] = new_val
        else:
            tmp_dat[new_label][tmp_dat[org_lb] == org_val] = new_val

        return tmp_dat

    def update_one(self, label, value, new_label=None, new_value=None, **kwargs):
        tmp = self.data.copy()
        tmp = self._update(tmp, label, value, new_label, new_value)
        self.apply(tmp, **kwargs)

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
        row_list = tmp[tmp[label] == value].index.tolist()
        tmp.drop(row_list, inplace=True, **kwargs)
        self.apply(tmp)

    def insert_one(self, data: pandas.DataFrame, **kwargs):
        tmp = self.data.copy()
        tmp = tmp.append(data, ignore_index=True)
        self.apply(tmp, **kwargs)

    def is_contain(self, label, val):
        tmp = self.data.copy()
        return bool(tmp[tmp[label] == val].index.tolist())


if __name__ == '__main__':
    pass
