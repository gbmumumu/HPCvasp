#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.spath import SPath


class OUTCAR:
    def __init__(self, outcar: SPath):
        self.outcar = outcar

    def read(self):
        for line in self.outcar.readline_text():
            pass



if __name__ == '__main__':
    pass
