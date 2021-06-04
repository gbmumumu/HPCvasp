#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique
from utils.spath import SPath
from calculation.vasp.inputs import INCAR, KPOINTS, KPOINTSModes


@unique
class Errors(Enum):
    calc_error = {
        1: ""
    }
    odd_behavior = {
        1: ""
    }
    system_fortran_error = {
        1: ""
    }
    tianhe_error = {
        1: ""
    }
    vasp_error = {
        1: ""
    }
    warning = {
        1: ""
    }

    @property
    def error_type(self):
        return self.value


class ErrType:
    def __init__(self, running_dir: SPath):
        self.running_root = running_dir

    @staticmethod
    def _match(target_file: SPath):
        match_results = []
        for e in Errors:
            for code, keyword in e.items():
                for line in target_file.readline_text_reversed():
                    if keyword in line:
                        match_results.append(code)
                        break
        return match_results

    def match(self):
        for log in ["yh.log", "OUTCAR", "OSZICAR"]:
            tf = self.running_root / log
            res = self._match(tf)
            if res:
                return res
        return None

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

    def try_to_adjust(self):
        if self.match():
            for error in self.match():
                pass

        return


if __name__ == '__main__':
    pass
