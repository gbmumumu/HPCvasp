#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from calculation.vasp.workflow import VaspRunningJob
from calculation.vasp.inputs import INCAR, POSCAR, KPOINTS, KPOINTSModes
from calculation.vasp.errors import ESkill
from utils.yhurm import TianHeJob, TianHeTime, TianHeWorker, TianHeNodes, TianHeJobManager
from utils.spath import SPath


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
    t = SPath(r"./test/calc/icsd_170660-Ta4Ga1Se8/Band")
    incar = t / "INCAR"
    kpoints = t / "KPOINTS"
    poscar = t / "POSCAR"

    e = ESkill(t)
    e.modify_kpoints(new_k_val=66)
