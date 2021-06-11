#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from multiprocessing.pool import Pool

from calculation.vasp.job import VaspRunningJob
from utils.yhurm import TianHeJob, TianHeTime, TianHeWorker, TianHeNodes, TianHeJobManager
from utils.spath import SPath


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


@click.group()
def main():
    pass


if __name__ == '__main__':
    main.add_command(converge)
    main.add_command(spin)
    main.add_command(errors)
    main.add_command(show_errors_from)
    main.add_command(get_inputs)
    main()
