#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from time import sleep
    from utils.spath import SPath
    from hpc import yhurm
    from utils.tools import LogCsv

    v = yhurm.TianHeJob(job_id=17123506).get_time()
    pz = yhurm.TianHeWorker().yield_time_limit_exceed_jobs()
