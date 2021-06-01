#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import seekpath

from utils.spath import SPath
from calculation.vasp.inputs import POSCAR


class KPOINTS:
    def __init__(self, mode, mesh, shift=(0, 0, 0), path=None):
        self.mode = mode
        self.mesh = mesh
        self.shift = shift
        self.path = path

    def __repr__(self):
        pass

    @classmethod
    def from_file(cls, filepath):
        pass

    def get_kmesh(self, poscar: POSCAR):
        pass

    def get_hk_path(self, poscar: POSCAR):
        pass

    def write(self):
        pass


if __name__ == '__main__':
    pass
