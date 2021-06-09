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

    def parser(self, job_name, job_paras):
        flow = ''
        task_dir = self.work_root / job_name
        converge_txt = task_dir / "converge.txt"
        spin_txt = task_dir / "is_spin.txt"
        flow += f"echo \'start {job_name} task\'"
        flow += f"mkdir {job_name} && cd {job_name}\n"
        node = job_paras.get("node")
        core = job_paras.get("core")
        if node is None:
            node = 1
            core = 24
        if core is None:
            core = 24 * node
        try_keyword = "try_num"
        try_num = job_paras.get(try_keyword)
        if try_num is None:
            try_num = 1
        parent = job_paras.get("parent")
        flow += f"echo \'prepare {job_name} inputs.\'"
        if parent is not None:
            flow += f"if [ -a {spin_txt}]; then\n"
            flow += f"  cp {spin_txt} ./"
            flow += f"fi"
        # 根据是否存在父任务及父任务结果准备输入文件
        flow += f"python {self._py} "
        flow += f"for ((try_num=0;try_num<={try_num};try_num++))\n"
        flow += "  do\n"
        flow += f"  echo \' round: {try_num} on {node} node {core} core\'"
        flow += f"  {self.yhrun_prog(node, core)} > yh.log\n"
        flow += f"  if [ $? -eq 0 ]; then\n"
        flow += f"    echo \'calc success\'\n"
        flow += f"    python {self._py} --work_dir\n" # 检查是否收敛, 没有则根据错误信息自动调整参数
        flow += f"    if [ -f \"{converge_txt}\" ];then\n"
        flow += f"      break\n"
        flow += f"    fi\n"
        flow += f"  fi\n"
        flow += f"  echo \'calc failed!\'\n"
        flow += f"  \n"

        flow += f"  "


class VaspRunningJob:
    def __init__(self, calc_dir: SPath):
        self.calc_dir = calc_dir
        self.poscar = self.calc_dir / "POSCAR"
        self.contcar = self.calc_dir / "CONTCAR"
        self.incar = self.calc_dir / "INCAR"
        self.kpoints = self.calc_dir / "KPOINTS"
        self.outcar = self.calc_dir / "OUTCAR"
        self.oszicar = self.calc_dir / "OSZICAR"
        self.incar = self.calc_dir / "INCAR"

    def is_spin(self):
        oszicar = self.calc_dir / "OSZICAR"
        final_mag = OSZICAR(oszicar).final_mag
        if final_mag is not None:
            if abs(final_mag) > 0.004:
                is_spin = self.calc_dir / "is_spin.txt"
                is_spin.write_text(str(final_mag))
                return True
        return False

    def is_converge(self):
        result = OUTCAR(self.outcar)
        if result.finished():
            if result.converged() or INCAR.from_file(self.incar).get("ISIF") != 3:
                converge = self.calc_dir / "converge.txt"
                converge.touch()
                return True
        return False

    def is_finish(self):
        return OUTCAR(self.outcar).finished()

    def check_errors(self):
        pass

    def process_errors(self):
        pass

    def prepare_job(self, job_type):
        pass


if __name__ == '__main__':
    pass
