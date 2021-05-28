#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from time import sleep
    from utils.spath import SPath
    from hpc import yhurm
    from utils.tools import LogCsv

    v = yhurm.TianHeNodes(job_id=123).get_cn_from_log()
    print(v)