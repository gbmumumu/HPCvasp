#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from utils.spath import SPath
    from utils import yhurm
    from calculation.vasp.inputs import POSCAR
    from calculation.vasp.outputs.oszicar import OSZICAR

    v = yhurm.TianHeJob(job_id=17123506).get_time()
    pz = yhurm.TianHeWorker().yield_time_limit_exceed_jobs()

    tj = r"./.local/test.json"
    x = SPath(tj).read_json()
    zj = r"./.local/test.yaml"
    y = SPath(zj).read_yaml()

    z = SPath(r"./.local")
    poscar = z / "POSCAR"
    p = POSCAR.from_file(poscar)
    r = p.get_primitive()
    oz = z / "OSZICAR"
    o = OSZICAR(oz)
