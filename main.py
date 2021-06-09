#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from calculation.vasp.workflow import VaspRunningJob
from calculation.vasp.inputs import INCAR, POSCAR, KPOINTS, KPOINTSModes
from calculation.vasp.workflow.etype import ErrType
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
def check_errors(work_dir):
    return VaspRunningJob(work_dir).check_errors()


@click.command()
def process_errors(work_dir):
    return VaspRunningJob(work_dir).process_errors()


@click.command()
def prepare_job(work_dir, job_type):
    return VaspRunningJob(work_dir).prepare_job(job_type)


@click.group()
def main():
    pass


if __name__ == '__main__':
    main.add_command(converge)
    main.add_command(spin)
    main()
