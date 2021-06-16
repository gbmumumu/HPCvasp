#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from calculation.vasp.job import VaspRunningJob
from config import CONDOR
from utils.yhurm import TianHeJob, TianHeTime, TianHeWorker, TianHeNodes, TianHeJobManager
from utils.spath import SPath
from utils.tools import multi_run, init_job


@click.command()
@click.option("--work_dir", help="work directory")
def converge(work_dir):
    return VaspRunningJob(SPath(work_dir)).is_converge()


@click.command()
@click.option("--work_dir", help="work directory")
def spin(work_dir):
    return VaspRunningJob(SPath(work_dir)).is_spin()


@click.command()
@click.option("--work_dir", help="work directory")
def errors(work_dir):
    return VaspRunningJob(SPath(work_dir)).automatic_check_errors()


@click.command()
@click.option("--log_name", help="log filename")
@click.option("--work_dir", help="work directory")
def show_errors_from(work_dir, log_name):
    return VaspRunningJob(SPath(work_dir)).get_errors(log_name)


@click.command()
@click.option("--job_type", help="job type in work config")
@click.option("--work_dir", help="work directory")
def get_inputs(work_dir, job_type):
    return VaspRunningJob(SPath(work_dir)).get_inputs_file(job_type)


@click.command()
@click.option("--process", help="multiprocessing num, default: 4", default=4)
@click.option("--pat", help="structure files type, default: *.vasp",
              default=f"{CONDOR.get('STRU', 'SUFFIX')}")
@click.option("--stru_dir", help="structure files directory",
              default=f"{CONDOR.get('STRU', 'PATH')}")
def prepare_task(stru_dir, pat, process=4):
    return TianHeJobManager(SPath(stru_dir)).init_jobs(pat=pat, n=process)


@click.group()
def main():
    pass


if __name__ == '__main__':
    main.add_command(converge)
    main.add_command(spin)
    main.add_command(errors)
    main.add_command(show_errors_from)
    main.add_command(get_inputs)
    main.add_command(prepare_task)
    main()
