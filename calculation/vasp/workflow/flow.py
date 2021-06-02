#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from config import WORKFLOW, CONDOR
from utils.spath import SPath
from calculation.vasp.outputs import OUTCAR, OSZICAR
from calculation.vasp.inputs import INCAR, KPOINTS, POSCAR, POTCAR


class WorkflowParser:
    def __init__(self, comment=None, source=None,
                 modules=None, workflow=None, prog=None):
        if comment is None:
            comment = "#!/bin/bash"
        self.comment = comment
        if prog is None:
            prog = "vasp_std"
        self.prog = prog
        if workflow is None:
            workflow = WORKFLOW
        self.workflow = workflow

    def yield_job(self):
        for job_name, job_paras in self.workflow.items():
            yield job_name, job_paras

    def yhrun_prog(self, node, core):
        return f"yhrun -N {node} -n {core} {CONDOR['VASP']['VASP_DIR']}/{self.prog}"

    def results_converge(self):
        pass

    def appear_errors(self):
        pass

    def modify_inputs(self):
        pass

    def parser(self, job_name, job_paras):
        flow = ''
        flow += f"mkdir {job_name} && cd {job_name}\n"
        node = job_paras.get("node")
        core = job_paras.get("core")
        if node is None:
            node = 1
            core = 24
        if core is None:
            core = 24 * node

        try_keyword = "try_num"
        if try_keyword in job_paras.keys():
            try_num = job_paras.get(try_keyword)
            if try_num is not None:
                flow += f"for ((try_num=0;try_num<={try_num};try_num++))\n"
                flow += "  do"
                flow += f"  {self.yhrun_prog(node, core)}"


class VaspRunningJob:
    def __init__(self, calc_dir: SPath):
        self.calc_dir = calc_dir
        self.poscar = self.calc_dir / "POSCAR"
        self.contcar = self.calc_dir / "CONTCAR"

        self.incar = self.calc_dir / "INCAR"
        self.kpoints = self.calc_dir / "KPOINTS"

    def is_spin(self):
        oszicar = self.calc_dir / "OSZICAR"
        if OSZICAR(oszicar).final_mag > 0.004:
            return True
        return False

    def is_converge(self):
        outcar = self.calc_dir / "OUTCAR"
        result = OUTCAR(outcar)
        return result.converged() and result.finished()

    def is_finish(self):
        outcar = self.calc_dir / "OUTCAR"
        return OUTCAR(outcar).finished()

    def check_errors(self):
        pass

    def process_errors(self):
        pass


if __name__ == '__main__':
    pass
