#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from queue import Queue
from calculation.vasp.job import VaspRunningJob
from calculation.npc import Submitter, Producer, Npc
from config import CONDOR
from utils.yhurm import TianHeJob, TianHeTime, TianHeWorker, TianHeNodes
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
def match(work_dir, log_name):
    return VaspRunningJob(SPath(work_dir)).get_errors(log_name)


@main.command()
@click.option("--work_dir", help="work directory")
def gif(work_dir):
    return VaspRunningJob(SPath(work_dir)).get_inputs_file()


@main.command()
@click.option("--work_dir", help="work directory")
def uif(work_dir):
    return VaspRunningJob(SPath(work_dir)).update_input_files()


@main.command()
def flush():
    control_paras = {
        "partition": CONDOR.get("ALLOW", "PARTITION"),
        "total_allowed_node": CONDOR.getint("ALLOW", "TOTAL_NODE"),
    }
    worker = TianHeWorker(**control_paras)
    worker.flush()


@main.command()
@click.option("--stime", help="interval time(sec) between submit job", default=0.5)
@click.option("--qsize", help="queue size, default: 20", default=20)
@click.option("--process", help="multiprocessing num, default: 4", default=4)
@click.option("--pat", help="structure files type, default: *.vasp",
              default=f"{CONDOR.get('STRU', 'SUFFIX')}")
@click.option("--stru_dir", help="structure files directory",
              default=f"{CONDOR.get('STRU', 'PATH')}")
def run(stru_dir, pat, process=4, qsize=20, stime=0.5):
    job_queue = Queue(maxsize=qsize)
    control_paras = {
        "partition": CONDOR.get("ALLOW", "PARTITION"),
        "total_allowed_node": CONDOR.getint("ALLOW", "TOTAL_NODE"),
    }
    worker = TianHeWorker(**control_paras)
    worker.flush()
    mana = Npc(SPath(stru_dir), interval_time=stime, )
    mana.init_jobs(pat, process)
    producer = Producer(queue=job_queue)
    submitter = Submitter(queue=job_queue, worker=worker)

    producer.start()
    submitter.start()
    worker.flush()


if __name__ == '__main__':
    main()
