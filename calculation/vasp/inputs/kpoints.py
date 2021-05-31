#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.spath import SPath


class KPOINTS:
    def __init__(self, mode, mesh, shift=(0, 0, 0), path=None):
        self.mode = mode
        self.mesh = mesh
        self.shift = shift
        self.path = path

    @classmethod
    def from_file(cls, filepath):
        pass


if __name__ == '__main__':
    pass
