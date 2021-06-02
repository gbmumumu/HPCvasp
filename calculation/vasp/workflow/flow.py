#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from config import WORKFLOW, CONDOR, PACKAGE_ROOT
from utils.spath import SPath
from calculation.vasp.outputs import OUTCAR, OSZICAR
from calculation.vasp.inputs import INCAR, KPOINTS, POSCAR, POTCAR


class WorkflowParser:
    def __init__(self,  work_root: SPath, comment=None, source=None,
                 modules=None, workflow=None, prog=None):
        self.work_root = work_root
        if comment is None:
            comment = "#!/bin/bash"
        self.comment = comment
        if prog is None:
            prog = "vasp_std"
        self.prog = prog
        if workflow is None:
            workflow = WORKFLOW
        self.workflow = workflow
        self._py = PACKAGE_ROOT / "main.py"

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
        task_dir = self.work_root / job_name
        flow += f"echo \'start {job_name} task\'"
        flow += f"mkdir {job_name} && cd {job_name}\n"
        node = job_paras.get("node")
        core = job_paras.get("core")
        if node is None:
            node = 1
            core = 24
        if core is None:
            core = 24 * node
        flow += f"echo \'prepare {job_name} inputs.\'"
        try_keyword = "try_num"
        try_num = job_paras.get(try_keyword)
        if try_num is None:
            try_num = 1

        flow += f"for ((try_num=0;try_num<={try_num};try_num++))\n"
        flow += "  do\n"
        flow += f"  echo \' round: {try_num} on {node} node {core} core\'"
        flow += f"  {self.yhrun_prog(node, core)}\n"
        flow += f"  python {self._py}\n"
        flow += f"  "


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
