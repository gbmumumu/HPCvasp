#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calculation.vasp.inputs import POSCAR
from utils.spath import SPath
from utils.tools import get_output

DEFAULT_PP = {}


class POTCAR:
    def __init__(self, lib: SPath):
        self.lib = lib

    def _cat_by(self, pel, des):
        return get_output(
            f"cat {self.lib / pel / 'POTCAR'} >> {des}"
        )

    @staticmethod
    def _get_pp(element):
        pass

    def cat(self, poscar: POSCAR, potcar):
        for element in poscar.symbol:
            self._cat_by(
                element, potcar
            )


if __name__ == '__main__':
    pass
