#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from calculation.vasp.job import VaspRunningJob
from config import CONDOR
from utils.yhurm import TianHeJob, TianHeTime, TianHeWorker, TianHeNodes, TianHeJobManager
from utils.spath import SPath


@click.group()
def main():
    pass


@main.command()
@click.option("--work_dir", help="work directory")
def converge(work_dir):
    return VaspRunningJob(SPath(work_dir)).is_converge()


@main.command()
@click.option("--work_dir", help="work directory")
def spin(work_dir):
    return VaspRunningJob(SPath(work_dir)).is_spin()


@main.command()
@click.option("--work_dir", help="work directory")
def errors(work_dir):
    return VaspRunningJob(SPath(work_dir)).automatic_check_errors()


@main.command()
@click.option("--log_name", help="log filename")
@click.option("--work_dir", help="work directory")
def show_errors_from(work_dir, log_name):
    return VaspRunningJob(SPath(work_dir)).get_errors(log_name)


@main.command()
@click.option("--job_type", help="job type in work config")
@click.option("--work_dir", help="work directory")
def get_inputs(work_dir, job_type):
    return VaspRunningJob(SPath(work_dir)).get_inputs_file(job_type)


@main.command()
@click.option("--process", help="multiprocessing num, default: 4", default=4)
@click.option("--pat", help="structure files type, default: *.vasp",
              default=f"{CONDOR.get('STRU', 'SUFFIX')}")
@click.option("--stru_dir", help="structure files directory",
              default=f"{CONDOR.get('STRU', 'PATH')}")
def prepare_task(stru_dir, pat, process=4):
    return TianHeJobManager(SPath(stru_dir)).init_jobs(pat=pat, n=process)


if __name__ == '__main__':
    main()
