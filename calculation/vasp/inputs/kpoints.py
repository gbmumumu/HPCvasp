#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import seekpath

from utils.spath import SPath
from calculation.vasp.inputs import POSCAR


class KPOINTS:
    def __init__(self, title="MATGEN KPT", mode=None, mesh=None, shift=(0, 0, 0), path=None):
        self.title = title
        self.mode = mode
        self.mesh = mesh
        self.shift = shift
        self.path = path

    def __repr__(self):
        pass

    @classmethod
    def from_file(cls, filepath: SPath, **kwargs):
        for line in filepath.readline_text(**kwargs):
            pass

    def get_kmesh(self, poscar: POSCAR):
        va, vb, vc = poscar.lattice.lattice


    def get_hk_path(self, poscar: POSCAR):
        pass

    def write(self):
        pass


if __name__ == '__main__':
    pass
