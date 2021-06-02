#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from calculation.vasp.workflow import VaspRunningJob


@click.command()
def is_converge(work_dir):
    return VaspRunningJob(work_dir).is_converge()


@click.command()
def is_finish(work_dir):
    return VaspRunningJob(work_dir).is_finish()


@click.command()
def is_spin(work_dir):
    return VaspRunningJob(work_dir).is_spin()


@click.command()
def check_errors(work_dir):
    return VaspRunningJob(work_dir).check_errors()


@click.command()
def process_errors(work_dir):
    return VaspRunningJob(work_dir).process_errors()


@click.command()
def prepare_job(work_dir, job_type):
    return VaspRunningJob(work_dir).prepare_job(job_type)


if __name__ == '__main__':
    from utils.spath import SPath
    from utils import yhurm
    from calculation.vasp.inputs import POSCAR
    from calculation.vasp.outputs.oszicar import OSZICAR
    from calculation.vasp.outputs.outcar import OUTCAR

    from config import CONDOR, WORKFLOW, PACKAGE_ROOT

    print(PACKAGE_ROOT)
