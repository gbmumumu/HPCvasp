#!/bin/sh
exe_dir=/WORK/nscc-gz_material_1/ICSD_vasp/vasp
source /WORK/app/toolshs/cnmodule.sh
module load intel-compilers/15.0.1
yhrun -N 4 -n 96  ${exe_dir}/vasp_std