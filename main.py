#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from time import sleep
    from utils.spath import SPath
    from hpc import yhurm
    from utils.tools import LogCsv

    x = SPath(r"./.local/1.csv").absolute()
    t = LogCsv(x)
    print(t.data)
    t.drop_row_data('id', 1)
    print(t)

