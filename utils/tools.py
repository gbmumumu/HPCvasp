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
            if not exit_code:
                while number < max_retry:
                    sleep(inter_time)
                    number += 1
                    print(f'{number} times')
                    exit_code, results = func(*args, **kwargs)
                    if exit_code:
                        break
            return results

        return inner

    return decorator


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
    def _update(tmp_dat, org_lb, org_val, new_val):
        tmp_dat.loc[tmp_dat[org_lb] == org_val] = new_val
        return tmp_dat

    def update_one(self, label, value, new_value):
        tmp = self.data.copy()
        tmp = self._update(tmp, label, value, new_value)
        self.apply(tmp)

    def update_many(self, labels: list, values: list, new_values: list):
        tmp = self.data.copy()
        for idx, lb in enumerate(labels):
            tmp = self._update(tmp, lb, values[idx], new_values[idx])
        self.apply(tmp)

    def drop_one(self, label, value):
        tmp = self.data.copy()
        row_list = tmp[tmp[label] == value].index.tolist()
        tmp.drop(row_list, inplace=True)
        self.apply(tmp)

    def insert_one(self, data: pandas.DataFrame):
        tmp = self.data.copy()
        tmp = tmp.append(data, ignore_index=True)
        self.apply(tmp)


if __name__ == '__main__':
    pass
