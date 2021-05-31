#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from time import sleep
    from utils.spath import SPath
    from hpc import yhurm
    from utils.tools import LogCsv
    from calculation.vasp.errors.eskill import ESkill
    from calculation.vasp.inputs import INCAR

    v = yhurm.TianHeJob(job_id=17123506).get_time()
    pz = yhurm.TianHeWorker().yield_time_limit_exceed_jobs()

    tj = r"./.local/test.json"
    x = SPath(tj).read_json()
    zj = r"./.local/test.yaml"
    y = SPath(zj).read_yaml()

    z = SPath(r"./.local")
    incar = z / "INCAR"
    t = INCAR.from_file(incar)
    n = {'SYSYTEM': 'xyz', 'LDAUU': [1.2, 3.8], 'LDAU': True, 'LWAVE': True, 'NSW': 100,
         'EDIFF': 0.0001}

    k = INCAR(**n)
    k.write(z/ "INCAR")