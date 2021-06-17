#!/bin/bash
source /WORK/app/toolshs/cnmodule.sh
module intel-compilers/15.0.1 MPI/Intel/MPICH/3.2-icc2018-dyn
echo 'start Test_spin task'
mkdir Test_spin && cd Test_spin || exit
echo 'prepare Test_spin inputs.'
python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin --job_type Test_spin
for ((try_num=1;try_num<=3;try_num++))
  do
  echo ' round: 3 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/nscc-gz_sgao/apps/bins/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 3 completed!'
    echo 'check calculation result...'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py converge --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin
    if [ -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin/converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin
  fi
  echo 'calculation not done, prepare to next loop'
  python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin
done
if [ ! -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Test_spin/converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Relax task'
mkdir Relax && cd Relax || exit
echo 'prepare Relax inputs.'
python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax --job_type Relax
for ((try_num=1;try_num<=5;try_num++))
  do
  echo ' round: 5 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/nscc-gz_sgao/apps/bins/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 5 completed!'
    echo 'check calculation result...'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py converge --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax
    if [ -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax/converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax
  fi
  echo 'calculation not done, prepare to next loop'
  python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax
done
if [ ! -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Relax/converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Scf task'
mkdir Scf && cd Scf || exit
echo 'prepare Scf inputs.'
python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf --job_type Scf
for ((try_num=1;try_num<=2;try_num++))
  do
  echo ' round: 2 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/nscc-gz_sgao/apps/bins/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 2 completed!'
    echo 'check calculation result...'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py converge --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf
    if [ -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf/converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf
  fi
  echo 'calculation not done, prepare to next loop'
  python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf
done
if [ ! -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Scf/converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Band task'
mkdir Band && cd Band || exit
echo 'prepare Band inputs.'
python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band --job_type Band
for ((try_num=1;try_num<=2;try_num++))
  do
  echo ' round: 2 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/nscc-gz_sgao/apps/bins/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 2 completed!'
    echo 'check calculation result...'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py converge --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band
    if [ -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band/converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band
  fi
  echo 'calculation not done, prepare to next loop'
  python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band
done
if [ ! -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Band/converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Dos task'
mkdir Dos && cd Dos || exit
echo 'prepare Dos inputs.'
python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos --job_type Dos
for ((try_num=1;try_num<=2;try_num++))
  do
  echo ' round: 2 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/nscc-gz_sgao/apps/bins/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 2 completed!'
    echo 'check calculation result...'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py converge --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos
    if [ -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos/converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py errors --work_dir /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos
  fi
  echo 'calculation not done, prepare to next loop'
  python /WORK/nscc-gz_sgao/matgen_dft/eht2/main.py get-inputs /WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos
done
if [ ! -f "/WORK/nscc-gz_sgao/matgen_dft/eht2/test/icsd_89414-Si8/Dos/converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
