#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from calculation.vasp.outputs import OUTCAR, OSZICAR
from calculation.vasp.inputs import INCAR, KPOINTS, POSCAR, POTCAR, KPOINTSModes
from calculation.vasp.workflow import ErrType
from config import WORKFLOW, CONDOR, INCAR_TEMPLATE
from utils.spath import SPath
from utils.yhurm import RUNNING_JOB_LOG
from utils.tools import smart_fmt


class VaspRunningJob:
    def __init__(self, calc_dir: SPath):
        self.calc_dir = calc_dir
        self._poscar = self.calc_dir / "POSCAR"
        self._contcar = self.calc_dir / "CONTCAR"
        self._incar = self.calc_dir / "INCAR"
        self._kpoints = self.calc_dir / "KPOINTS"
        self._outcar = self.calc_dir / "OUTCAR"
        self._oszicar = self.calc_dir / "OSZICAR"
        self._incar = self.calc_dir / "INCAR"
        self._potcar = self.calc_dir / "POTCAR"

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
        result = OUTCAR(self._outcar)
        if result.finished():
            if result.converged() or INCAR.from_file(self._incar).get("ISIF") != 3:
                converge = self.calc_dir / "converge.txt"
                converge.touch()
                return True
        return False

    def is_finish(self):
        return OUTCAR(self._outcar).finished()

    @property
    def job_id(self):
        _id = self.get_job_id_from_log()
        if _id is not None:
            return _id
        job_ids = self.get_job_ids_from_slurm_file()
        if job_ids:
            return max(job_ids)
        raise FileNotFoundError("Slurm log not found!")

    def get_job_ids_from_slurm_file(self):
        slurm_ids = []
        regex = re.compile(r"\d+")
        for file in self.calc_dir.parent.rglob("slurm*.out"):
            slurm_ids.extend(
                regex.findall(file.name)
            )
        return [int(i) for i in slurm_ids]

    def get_job_id_from_log(self):
        if RUNNING_JOB_LOG.is_contain("WORKDIR", self.calc_dir):
            return RUNNING_JOB_LOG.get("WORKDIR", self.calc_dir)["JOBID"]
        return None

    def automatic_check_errors(self):
        e = ErrType(job_id=self.job_id, running_dir=self.calc_dir)
        e.automatic_error_correction()

    def get_errors(self, error_log):
        e = ErrType(job_id=self.job_id, running_dir=self.calc_dir)
        errors = list(e.get_error_from(self.calc_dir / error_log))
        if not errors:
            print(f"error not found from {error_log}")
        for item, _ in errors:
            print(f"error type: {item.value}")
        return errors

    def get_inputs_file(self, job_type):
        job_info = WORKFLOW[job_type]
        last_job = job_info.get("parent")
        incar_paras = INCAR_TEMPLATE.get(job_type)
        assert incar_paras is not None
        incar = INCAR(**incar_paras)
        if last_job is not None:
            last_job_path = self.calc_dir.parent / last_job
            last_job_files = job_info.get("parent_files")
            spin_txt = last_job_path / "is_spin.txt"
            if spin_txt.exists():
                incar["ISPIN"] = 2
                spin_txt.copy_to(self.calc_dir)
            if last_job_files:
                for filename in last_job_files:
                    file = last_job_path / filename
                    if filename == "CONTCAR":
                        file.copy_to(self.calc_dir / "POSCAR")
                    else:
                        file.copy_to(self.calc_dir)
        else:
            incar["ISPIN"] = 2
            sfx = CONDOR.get("STRU", "SUFFIX")
            for _poscar in self.calc_dir.parent.walk(pattern=f"*{sfx}"):
                _poscar.copy_to(self.calc_dir / "POSCAR")
        assert self._poscar.exists()
        stru = POSCAR.from_file(self._poscar)
        hubbard_u = stru.get_hubbard_u_if_need()
        if hubbard_u is not None:
            for lb, v in hubbard_u.items():
                incar[lb] = v
        incar.write(self._incar)

        if not self._potcar.exists():
            potcar_lib = CONDOR.get("VASP", "PSEUDO_POTENTIAL_DIR")
            if not SPath(potcar_lib).exists():
                raise FileNotFoundError("POTCAR Source not found!")
            POTCAR(lib=potcar_lib).cat(stru, self._potcar)
        kpt_type, *kpt_paras = job_info.get("kpt")
        try_num = job_info.get("try_num")
        if try_num is None:
            try_num = 2
        if len(kpt_paras) < try_num:
            kpt_paras.extend([kpt_paras[-1], ] * (try_num - len(kpt_paras)))
        else:
            kpt_paras = kpt_paras[:try_num]
        run_time_txt = self.calc_dir / "running"
        if not run_time_txt.exists():
            run_time_txt.write_text(data=f"{1}")
            kpt_para = kpt_paras[0]
        else:
            run_time = smart_fmt(run_time_txt.read_text())
            kpt_para = kpt_paras[run_time]
            run_time_txt.write_text(data=f"{run_time + 1}")
        kpt_style = KPOINTSModes.from_string(kpt_type)
        if kpt_style == KPOINTSModes.LineMode:
            kpoints = KPOINTS(interval_of_kpoints=kpt_para, style=kpt_style)
            kpoints.get_hk_path(stru)
        else:
            kpoints = KPOINTS(style=kpt_style)
            kpoints.get_kmesh(stru, kpt_para)
        kpoints.write(self._kpoints)


if __name__ == '__main__':
    pass
