#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getstatusoutput
from time import sleep
import pandas
from multiprocessing.pool import Pool

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


def smart_fmt(inputs):
    if isinstance(inputs, str):
        if inputs.isalpha():
            return inputs
        else:
            if '.' in inputs or 'e' in inputs or 'E' in inputs:
                return float(inputs)
            return int(inputs)
    if isinstance(inputs, list) or isinstance(inputs, tuple):
        return [smart_fmt(i) for i in inputs]

    raise TypeError


def multi_run(generator, func, n, *args, **kwargs):
    pool = Pool(n)
    results = []
    for item in generator:
        results.append(
            pool.apply_async(func, args=(item,), *args, **kwargs)
        )

    pool.close()
    pool.join()
    for r in results:
        try:
            yield r.get()
        except:
            continue


class LogCsv:
    def __init__(self, csv: SPath):
        self._path = csv

    def __repr__(self):
        return str(self._path)

    @property
    def csv(self):
        self._csv = None
        if self._path.exists():
            self._csv = pandas.read_csv(self._path, sep="\t")

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


if __name__ == '__main__':
    pass
