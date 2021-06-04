#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique
from utils.spath import SPath
from calculation.vasp.inputs import INCAR, KPOINTS, KPOINTSModes


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

    @property
    def error_type(self):
        return self.value

    def __str__(self):
        return self.name


class ErrType:
    errorType = Errors

    def __init__(self, running_dir: SPath):
        self.running_root = running_dir

    @staticmethod
    def _match(target_file: SPath):
        for e in Errors:
            for code, keyword in e.items():
                for line in target_file.readline_text_reversed():
                    if keyword in line:
                        yield str(e), code

    def match(self):
        for log in ["yh.log", "OUTCAR", "OSZICAR"]:
            yield self._match(
                self.running_root / log
            )

    def modify_incar(self, **kwargs):
        incar_fp = self.running_root / "INCAR"
        incar = INCAR.from_file(incar_fp)
        for key, item in kwargs.items():
            incar[key] = item

        incar.write(incar_fp)

    def modify_kpoints(self, new_k_val=20, new_k_mesh=0.04):
        poscar_fp = self.running_root / "CONTCAR"
        kpt_fp = self.running_root / "KPOINTS"
        if poscar_fp.is_empty():
            poscar_fp = self.running_root / "POSCAR"
        kpt = KPOINTS.from_file(kpt_fp)
        if kpt.style in [KPOINTSModes.Gamma, KPOINTSModes.Monkhorst]:
            kpt.get_kmesh(poscar_fp, new_k_mesh)
        if kpt.style == KPOINTSModes.LineMode:
            kpt.nkpt = new_k_val

        kpt.write(kpt_fp)

    def update_poscar(self):
        contcar = self.running_root / "CONTCAR"
        poscar = self.running_root / "POSCAR"
        contcar.copy_to(poscar)

    def modify_potcar(self):
        pass

    def _reaction(self, error_code):
        pass

    def modify_input_based_on_error(self, error):
        while True:
            try:
                if self.match():
                    for error in self.match():
                        self._reaction(error)
            except StopIteration:
                break


if __name__ == '__main__':
    pass
