#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from utils.spath import SPath
from utils.tools import smart_fmt


class OSZICAR:
    def __init__(self, filepath: SPath):
        self.osizcar = filepath

    def __len__(self):
        return len(self.read())

    def __getitem__(self, item):
        return self.read()[item]

    def read(self):
        steps, idx = [], 1
        regex = re.compile(r"(\d+\s|-?.?\d+.?E?[+|-]?\d+)")
        for line in self.osizcar.readline_text():
            if "F=" in line:
                p = regex.findall(line)
                idx, *p = [smart_fmt(i) for i in p]
                h = ["F", "E0", "dE", "mag"]
                steps.append(
                    {
                        idx: dict(zip(h, p))
                    }
                )

        return steps

    @property
    def final_step(self):
        return self.read()[-1].get(len(self))

    @property
    def final_energy(self):
        return self.final_step.get("E0")

    @property
    def final_diff_energy(self):
        return self.final_step.get("dE")

    @property
    def final_total_mag(self):
        return self.final_step.get("mag")


if __name__ == '__main__':
    pass
