#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calculation.vasp.inputs import INCAR, KPOINTS, KPOINTSModes
from utils.spath import SPath


class Skill:
    def __init__(self, running_dir: SPath):
        self.running_root = running_dir

    def modify_incar(self, **kwargs):
        incar_fp = SPath(self.running_root / "INCAR")
        incar = INCAR.from_file(incar_fp)
        for key, item in kwargs.items():
            incar[key] = item

        incar.write(incar_fp)

    def modify_kpoints(self, new_k_val=20, new_k_mesh=0.04):
        poscar_fp = SPath(self.running_root / "CONTCAR")
        kpt_fp = SPath(self.running_root / "KPOINTS")
        if poscar_fp.is_empty():
            poscar_fp = SPath(self.running_root / "POSCAR")
        kpt = KPOINTS.from_file(kpt_fp)
        if kpt.style in [KPOINTSModes.Gamma, KPOINTSModes.Monkhorst]:
            kpt.get_kmesh(poscar_fp, new_k_mesh)
        if kpt.style == KPOINTSModes.LineMode:
            kpt.nkpt = new_k_val

        kpt.write(kpt_fp)

    def update_poscar(self):
        contcar = SPath(self.running_root / "CONTCAR")
        poscar = SPath(self.running_root / "POSCAR")
        contcar.copy_to(poscar)

    def modify_potcar(self):
        pass


if __name__ == '__main__':
    pass
