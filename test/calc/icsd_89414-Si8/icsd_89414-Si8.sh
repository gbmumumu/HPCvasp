#!/bin/bash
source /WORK/app/toolshs/cnmodule.sh
module load MPI/Intel/MPICH/3.2-icc14-dyn
module load intel-compilers/15.0.1
exe_dir=/WORK/nscc-gz_material_1/ICSD_vasp/vasp
python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8 2

cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
signal=0
while [ "$signal" -le 5 ]
do echo "enter check loop $signal: /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax"
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax -1 $signal
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/no_convergence.txt ];then
    echo 'copy CONTCAR to POSCAR'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax -2
    echo contcar2poscar > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/rerun.txt
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/no_convergence.txt
  fi
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax 9
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/appear_err_msg.txt ];then
    echo 'error msg appears'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax 6
  fi
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/rerun.txt ];then
    cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/rerun.txt
  else
    break
  fi
  signal=`expr $signal + 1`
done

python run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax 0
if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Relax/rerun.txt ];then
  exit 0
fi
python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8 3

cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
signal=0
while [ "$signal" -le 2 ]
do echo "enter check loop $signal: /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf"
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf -1 $signal
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/no_convergence.txt ];then
    echo 'copy CONTCAR to POSCAR'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf -2
    echo contcar2poscar > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/rerun.txt
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/no_convergence.txt
  fi
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf 9
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/appear_err_msg.txt ];then
    echo 'error msg appears'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf 6
  fi
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/rerun.txt ];then
    cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/rerun.txt
  else
    break
  fi
  signal=`expr $signal + 1`
done

python run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf 0
if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Scf/rerun.txt ];then
  exit 0
fi
python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8 4

cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
signal=0
while [ "$signal" -le 2 ]
do echo "enter check loop $signal: /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band"
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band -1 $signal
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/no_convergence.txt ];then
    echo 'copy CONTCAR to POSCAR'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band -2
    echo contcar2poscar > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/rerun.txt
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/no_convergence.txt
  fi
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band 9
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/appear_err_msg.txt ];then
    echo 'error msg appears'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band 6
  fi
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/rerun.txt ];then
    cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/rerun.txt
  else
    break
  fi
  signal=`expr $signal + 1`
done

python run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band 0
if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Band/rerun.txt ];then
  exit 0
fi
python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8 5

cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
signal=0
while [ "$signal" -le 2 ]
do echo "enter check loop $signal: /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos"
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos -1 $signal
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/no_convergence.txt ];then
    echo 'copy CONTCAR to POSCAR'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos -2
    echo contcar2poscar > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/rerun.txt
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/no_convergence.txt
  fi
  python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos 9
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/appear_err_msg.txt ];then
    echo 'error msg appears'
    python /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts/run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos 6
  fi
  if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/rerun.txt ];then
    cd /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos;yhrun -n 48  ${exe_dir}/vasp_std > /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/yh.log;cd /WORK/nscc-gz_material_1/ICSD_vasp/scripts/gam-scripts;
    rm /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/rerun.txt
  else
    break
  fi
  signal=`expr $signal + 1`
done

python run_vasp.py /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos 0
if [ -a /WORK/nscc-gz_material_1/ICSD_vasp/simple_substance_work/rerun/icsd_89414-Si8/Dos/rerun.txt ];then
  exit 0
fi
