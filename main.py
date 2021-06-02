#!/usr/bin/env python3
# -*- coding: utf-8 -*-




if __name__ == '__main__':
    from utils.spath import SPath
    from utils import yhurm
    from calculation.vasp.inputs import POSCAR
    from calculation.vasp.outputs.oszicar import OSZICAR
    from calculation.vasp.outputs.outcar import OUTCAR

    from config import CONDOR, WORKFLOW

    print(CONDOR)
