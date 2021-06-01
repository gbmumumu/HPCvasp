#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import seekpath

from utils.spath import SPath
from utils.tools import smart_fmt
from calculation.vasp.inputs import POSCAR


class KPOINTS:
    def __init__(self, title="MATGEN KPT", generate_method=None, style=None, kmesh=None,
                 shift=(0, 0, 0), kpath=None):
        self.title = title
        self.gm = generate_method
        self.style = style
        self.kmesh = kmesh
        self.shift = shift
        self.kpath = kpath

    def __repr__(self):
        if self.kpath is None:
            return

        return

    @classmethod
    def from_file(cls, filepath: SPath, **kwargs):
        file = filepath.readline_text(**kwargs)
        title = next(file)
        num_kpt = smart_fmt(next(file))
        style = next(file).lower()
        if style[0] in ["g", "m"]:
            kmesh = [smart_fmt(i) for i in next(file).split()]
            shift = [smart_fmt(j) for j in next(file).split()]
        if style[0] == "r":
            pass





    def get_kmesh(self, poscar: POSCAR, mesh=0.02):
        va, vb, vc = poscar.lattice.reciprocal_lattice().lattice


    def get_hk_path(self, poscar: POSCAR):
        pass

    def write_kpoints(self):
        pass

    def write_kpath(self):
        pass


if __name__ == '__main__':
    pass
