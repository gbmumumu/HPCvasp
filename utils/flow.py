#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.spath import SPath


class Flow:
    def __init__(self, flow_file, apply_sh):
        if not isinstance(flow_file, SPath):
            self.flow_file = SPath(flow_file)
        if not isinstance(apply_sh, SPath):
            self.apply_sh = SPath(apply_sh)

    def eval(self, **kwargs):
        for line in self.flow_file.readline_text(**kwargs):
            pass

    def apply(self):
        pass


if __name__ == '__main__':
    pass
