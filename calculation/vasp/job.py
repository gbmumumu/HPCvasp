#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from calculation.vasp.outputs import OUTCAR, OSZICAR
from calculation.vasp.inputs import INCAR, KPOINTS, POSCAR, POTCAR
from calculation.vasp.workflow import ErrType
from utils.spath import SPath
from utils.yhurm import RUNNING_JOB_LOG


class VaspRunningJob:
    def __init__(self, calc_dir: SPath):
        self.calc_dir = calc_dir
        self.poscar = self.calc_dir / "POSCAR"
        self.contcar = self.calc_dir / "CONTCAR"
        self.incar = self.calc_dir / "INCAR"
        self.kpoints = self.calc_dir / "KPOINTS"
        self.outcar = self.calc_dir / "OUTCAR"
        self.oszicar = self.calc_dir / "OSZICAR"
        self.incar = self.calc_dir / "INCAR"

    def is_spin(self):
        oszicar = self.calc_dir / "OSZICAR"
        final_mag = OSZICAR(oszicar).final_mag
        if final_mag is not None:
            if abs(final_mag) > 0.004:
                is_spin = self.calc_dir / "is_spin.txt"
                is_spin.write_text(str(final_mag))
                return True
        return False

    def is_converge(self):
        result = OUTCAR(self.outcar)
        if result.finished():
            if result.converged() or INCAR.from_file(self.incar).get("ISIF") != 3:
                converge = self.calc_dir / "converge.txt"
                converge.touch()
                return True
        return False

    def is_finish(self):
        return OUTCAR(self.outcar).finished()

    @property
    def job_id(self):
        _id = self.get_job_id_from_log()
        if _id is not None:
            return _id
        job_ids = self.get_job_ids_from_slurm_file()
        if job_ids:
            return max(job_ids)
        raise FileNotFoundError("Slurm log not found!")

    def get_job_ids_from_slurm_file(self):
        slurm_ids = []
        regex = re.compile(r"\d+")
        for file in self.calc_dir.parent.rglob("slurm*.out"):
            slurm_ids.extend(
                regex.findall(file.name)
            )
        return [int(i) for i in slurm_ids]

    def get_job_id_from_log(self):
        if RUNNING_JOB_LOG.is_contain("WORKDIR", self.calc_dir):
            return RUNNING_JOB_LOG.get("WORKDIR", self.calc_dir)["JOBID"]
        return None

    def automatic_check_errors(self):
        e = ErrType(job_id=self.job_id, running_dir=self.calc_dir)
        e.automatic_error_correction()

    def get_errors(self, error_log):
        e = ErrType(job_id=self.job_id, running_dir=self.calc_dir)
        errors = e.get_error_from(self.calc_dir / error_log)
        if errors is None:
            print(f"error not found from {error_log}")
        return errors


if __name__ == '__main__':
    pass
