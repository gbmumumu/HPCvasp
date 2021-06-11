#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from config import WORKFLOW, CONDOR, PACKAGE_ROOT
from utils.spath import SPath


class WorkflowParser:
    def __init__(self, work_root: SPath, comment=None, source=None,
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
        flow += f"echo \'start {job_name} task\'"
        flow += f"mkdir {job_name} && cd {job_name}\n"
        node = job_paras.get("node")
        core = job_paras.get("core")
        if node is None:
            node = 1
            core = 24
        if core is None:
            core = 24 * node
        try_num = job_paras.get("try_num")
        if try_num is None:
            try_num = 1
        flow += f"echo \'prepare {job_name} inputs.\'"
        flow += f"python {self._py} get-inputs --work_dir {task_dir} --job_type {job_name}"
        flow += f"for ((try_num=1;try_num<={try_num};try_num++))\n"
        flow += "  do\n"
        flow += f"  echo \' round: {try_num} on {node} node {core} core\'"
        flow += f"  {self.yhrun_prog(node, core)} > yh.log\n"
        flow += f"  if [ $? -eq 0 ]; then\n"
        flow += f"    echo \'calc step: {try_num} completed!\'\n"
        flow += f"    echo \'check calculation result...\'\n"
        flow += f"    python {self._py} errors --work_dir {task_dir}\n"
        flow += f"    python {self._py} converge --work_dir {task_dir}\n"
        flow += f"    if [ -f \"{converge_txt}\" ];then\n"
        flow += f"      break\n"
        flow += f"    fi\n"
        flow += f"  else"
        flow += f"    echo \'yhrun command failed! check errors\'"
        flow += f"    python {self._py} errors --work_dir {task_dir}\n"
        flow += f"  fi\n"
        flow += f"  echo \'calculation not done, prepare to next loop\'\n"
        flow += f"  python {self._py} get-inputs {task_dir}"
        flow += f"if [ ! -f \"{converge_txt}\" ];then\n"
        flow += f"  echo \'The job in the specified setting is not completed, " \
                f"       and the subsequent tasks will not be performed\' \n"
        flow += f"  exit"
        flow += f"fi"


if __name__ == '__main__':
    pass
