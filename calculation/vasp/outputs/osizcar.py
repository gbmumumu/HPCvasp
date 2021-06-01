#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.spath import SPath


class OSIZCAR:
    def __init__(self, filepath: SPath):
        self.osizcar = filepath

    def flush(self):
        steps = []
        regex_lst = r"(\d+?)\s+?F.*E0=\s(.*)\s+d\sE\s=(.*)"
        for line in self.osizcar.readline_text():
            if "F=" in line:
                steps.append()


if __name__ == '__main__':
    pass
