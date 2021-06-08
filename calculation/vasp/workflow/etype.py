#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from enum import Enum, unique
from utils.spath import SPath
from calculation.vasp.inputs import INCAR, KPOINTS, KPOINTSModes
from utils.yhurm import TH_LOCAL, TianHeNodes, NPC, TianHeJob, ALL_JOB_LOG, RUNNING_JOB_LOG
from utils.tools import LogCsv
from config import WORKFLOW, CONDOR

ERROR_JOB_HEAD = ["JOB_PATH", "ERROR_CODE", "ERROR_NAME"]
ERROR_JOB_LOG = LogCsv(SPath(TH_LOCAL / "error_job.csv"))


@unique
class Errors(Enum):
    calc_error = {
        1: "ZBRENT: fatal error in bracketing please rerun with smaller EDIFF, or copy CONTCAR to POSCAR and continue"
    }
    odd_behavior = {
        2: "internal ERROR RSPHER:running out of buffer",
        3: "Hard potentials",
        4: "Suspicious behaviour of the local potential",
        5: "Large positive energies for vdW-DF functional "
    }
    system_fortran_error = {
        6: "exit status of rank 9: killed by signal 9",
        7: "integer divide by zero",
        8: "Calculation hangs at high k-point parallellization",
        9: "Fatal error in MPI_Allreduce: Message truncated, error stack",
        10: "Fatal error in PMPI_Allgatherv: Internal MPI error!, error stack "
    }
    tianhe_error = {
        11: "yhrun: error"
    }
    vasp_error = {
        12: "Error EDDDAV: Call to ZHEGV failed",
        13: "Error EDDRMM: Call to ZHEGV failed",
        14: "VERY BAD NEWS! internal error in subroutine INVGRP",
        15: "accuracy reached - accuracy cannot be reached",
        16: "ERROR: missing or invalid vector defining dimer",
        17: "No initial positions read in",
        18: "VERY BAD NEWS! internal error in subroutine PRICEL",
        19: "ERROR FEXCP: supplied Exchange-correletion table is too small",
        20: "Error code was IERR=5",
        21: "internal error in FOCK_ACC: number of k-points incorrect",
        22: "ERROR: there must be 1 or 3 items on line 2 of POSCAR",
        23: "internal error in RAD_INT: RHOPS /= RHOAE",
        24: "EDWAV: internal error, the gradient is not orthogonal",
        25: "LAPACK: Routine ZPOTRF failed!",
        26: "ERROR in subspace rotation PSSYEVX: not enough eigenvalues found",
        27: "VERY BAD NEWS! internal error in subroutine SGRGEN: Too many elements",
        28: "VERY BAD NEWS! internal error in subroutine SGRCON: Found some non-integer element in rotation matrix"
    }
    tips = {
        29: "BRIONS problems: POTIM should be increased"
    }

    @property
    def error_type(self):
        return self.value

    def __str__(self):
        return self.name


class ErrType:
    errorType = Errors

    def __init__(self, job_id, running_dir: SPath):
        self.job_id = job_id
        self.running_root = running_dir
        self.yh = self.running_root / "yh.log"
        self._outcar = self.running_root / "OUTCAR"
        self._incar = self.running_root / "INCAR"
        self._oszicar = self.running_root / "OSZICAR"
        self._contcar = self.running_root / "CONTCAR"
        self._kpoints = self.running_root / "KPOINTS"
        self._poscar = self.running_root / "POSCAR"
        self._chgcar = self.running_root / "CHGCAR"

    @property
    def workflow_type(self):
        return self.running_root.name

    @property
    def incar(self):
        return INCAR.from_file(self._incar)

    @property
    def kpoints(self):
        return KPOINTS.from_file(self._kpoints)

    def update_incar(self, **kwargs):
        for key, item in kwargs.items():
            self.incar[key] = item

    def update_kpoints(self, new_k_val=20, new_k_mesh=0.04):
        if self.kpoints.style in [KPOINTSModes.Gamma, KPOINTSModes.Monkhorst]:
            if not self._contcar.is_empty():
                self.kpoints.get_kmesh(self._contcar, new_k_mesh)
            else:
                self.kpoints.get_kmesh(self._poscar, new_k_mesh)
        if self.kpoints.style == KPOINTSModes.LineMode:
            self.kpoints.nkpt = new_k_val

        self.kpoints.write(self._kpoints)

    def contcar2poscar(self):
        self._contcar.copy_to(self._poscar)

    def modify_potcar(self):
        raise NotImplementedError

    @staticmethod
    def _match(target_file: SPath):
        for e in Errors:
            for code, keyword in e.value.items():
                for line in target_file.readline_text_reversed():
                    if keyword in line:
                        yield e, code

    def _yield_error(self):
        for log in [self.yh, self._outcar, self._oszicar]:
            matched = self._match(self.running_root / log)
            if matched is not None:
                yield matched

    def reaction(self, err_type, err_code):
        if err_code == 1:
            print(f"error type: {err_type.value}, update POSCAR...")
            self.contcar2poscar()
        if err_code in (2, 3, 4, 5, 6, 7, 8):
            NPC.flush()
            if RUNNING_JOB_LOG.is_contain("JOBID", self.job_id):
                job_nodes = TianHeNodes(self.job_id)
                try:
                    job_nodes.kill_zombie_process_on_nodes(key_word=CONDOR["VASP"]["VASP_EXE"])
                except:
                    job = TianHeJob(job_id=self.job_id)
                    job.yhcancel()
                    RUNNING_JOB_LOG.drop_one("JOBID", self.job_id)
                    ALL_JOB_LOG.update_one("JOBID", self.job_id, "RESULT", "Failed")
        if err_code in (9, 10, 11):
            print(f"error type: {err_type.value}, "
                  f"High probability is a problem of parallel parameter setting ...")
            nnode = WORKFLOW[self.workflow_type]["node"]
            ncore = WORKFLOW[self.workflow_type]["core"]
            core_per_node = int(ncore / nnode)
            npar = int(math.sqrt(core_per_node))
            try:
                if self.incar["NPAR"] is not None:
                    if self.incar["NPAR"] == npar:
                        print(f"Oh, I have no idea about this...")
                else:
                    self.incar["NCORE"] = core_per_node
                    self.incar["NPAR"] = npar
            except (KeyError, TypeError):
                pass
            else:
                self.incar.write(self._incar)
        if err_code in (12, 13):
            if self._chgcar.exists():
                self._chgcar.rm_file()
            ialgo = self.incar["IALGO"]
            if ialgo is not None:
                if ialgo == 38:
                    self.incar["IALGO"] = 48
                if ialgo == 48:
                    self.incar["IALGO"] = 38
            else:
                algo = self.incar["ALGO"]
                if algo == "Normal":
                    self.incar["ALGO"] = "Fast"
                elif algo == "Fast":
                    self.incar["ALGO"] = "Very_Fast"
                else:
                    self.incar["ALGO"] = "Normal"
            if not self._contcar.is_empty():
                self.contcar2poscar()
            self.incar.write(self._incar)
        if err_code == 14:
            self.incar["ISYM"] = 0
            self.incar.write(self._incar)
        if err_code == 15:
            self.contcar2poscar()
        if err_code == 16:
            print("")
        if err_code == 17:
            pass

        if err_code == 29:
            print(f"error type: {err_type.value}, trying to increase INCAR POTIM para...")
            try:
                if self.incar["POTIM"] <= 0.1:
                    self.incar["POTIM"] = 0.5
                else:
                    self.incar["POTIM"] += 0.2
            except (KeyError, TypeError):
                self.incar["POTIM"] = 0.5
            finally:
                self.incar.write(self._incar)

    def automatic_error_correction(self):
        for x in self._yield_error():
            xl = list(x)
            if xl:
                for err_type, err_code in xl:
                    self.reaction(err_type, err_code)


if __name__ == '__main__':
    pass