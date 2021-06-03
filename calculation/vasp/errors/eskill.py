#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calculation.vasp.inputs import INCAR, KPOINTS, POTCAR
from utils.spath import SPath


class ESkill:
    def __init__(self, running_dir: SPath):
        self.running_root = running_dir

    def modify_incar(self, **kwargs):
        incar = INCAR.from_file(
            SPath(self.running_root / "INCAR")
        )
        for key, item in kwargs.items():
            incar[key] = item

        incar.write(SPath(
            self.running_root / "INCAR"
        ))

    def modify_kpoints(self, **kwargs):
        kpoints = KPOINTS.from_file(
            SPath(self.running_root / "KPOINTS")
        )
        for key, item in kwargs.items():
            kpoints[key] = item

        if kpoints.mode == 1:
            pass
        elif kpoints.mode == 2:
            pass

    def update_poscar(self):
        contcar = SPath(self.running_root / "CONTCAR")
        poscar = SPath(self.running_root / "POSCAR")
        contcar.copy_to(poscar)

    def modify_potcar(self):
        pass


if __name__ == '__main__':
    pass
