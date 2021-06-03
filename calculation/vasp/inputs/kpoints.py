#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from enum import Enum
import re

import seekpath
from utils.spath import SPath
from utils.tools import smart_fmt
from calculation.vasp.inputs import POSCAR


class KPOINTSModes(Enum):
    Gamma = 1
    Monkhorst = 2
    LineMode = 3

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        c = s.lower()[0]
        for m in KPOINTSModes:
            if m.name.lower()[0] == c:
                return m
        return None


class KPOINTS:
    mode = KPOINTSModes

    def __init__(self, title="MATGEN KPT", scheme=0, interval_of_kpoints=40, coord_type=None,
                 style=mode.Monkhorst, kmesh=(1, 1, 1), shift=(0, 0, 0), kpath=None, labels=None):
        self.title = title
        self.scheme = scheme
        self.interval_of_k = interval_of_kpoints
        self._style = style
        self.kmesh = kmesh
        self.shift = shift
        self.kpath = kpath
        self.labels = labels

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        if isinstance(style, str):
            style = KPOINTSModes.supported_modes.from_string(style)
        self._style = style

    @classmethod
    def from_file(cls, filepath: SPath, **kwargs):
        file = filepath.readline_text(**kwargs)
        title = next(file)
        num_kpt = smart_fmt(next(file))
        style = next(file).lower()
        # Fully automatic KPOINTS

        if style[0] in ["g", "m"]:
            style = KPOINTS.mode.from_string(style)
            kmesh = [smart_fmt(i) for i in next(file).split()]
            shift = [smart_fmt(j) for j in next(file).split()]
            return cls(title=title, style=style, kmesh=kmesh, shift=shift, scheme=num_kpt)
        if style == "l":
            style = KPOINTS.mode.LineMode
            coord_type = next(file)
            kpath = []
            labels = []
            patt = re.compile(r'([e0-9.\-]+)\s+([e0-9.\-]+)\s+([e0-9.\-]+)'
                              r'\s*!*\s*(.*)')
            while True:
                try:
                    line = next(file)
                except StopIteration:
                    break
                else:
                    m = patt.match(line)
                    if m:
                        kpath.append([smart_fmt(m.group(1)), smart_fmt(m.group(2)),
                                     smart_fmt(m.group(3))])
                        labels.append(m.group(4).strip())
            return cls(style=style, kpath=kpath, labels=labels,
                       interval_of_kpoints=num_kpt, coord_type=coord_type)

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
