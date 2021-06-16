#!/bin/bash
source /WORK/app/toolshs/cnmodule.sh
module intel-compilers/15.0.1
echo 'start Test_spin task'
mkdir Test_spin && cd Test_spin || exit
echo 'prepare Test_spin inputs.'
python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs --work_dir test\calc\n\Test_spin --job_type Test_spin
for ((try_num=1;try_num<=3;try_num++))
  do
  echo ' round: 3 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/app/condor/vasp/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 3 completed!'
    echo 'check calculation result...'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Test_spin
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py converge --work_dir test\calc\n\Test_spin
    if [ -f "test\calc\n\Test_spin\converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Test_spin
  fi
  echo 'calculation not done, prepare to next loop'
  python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs test\calc\n\Test_spin
done
if [ ! -f "test\calc\n\Test_spin\converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Relax task'
mkdir Relax && cd Relax || exit
echo 'prepare Relax inputs.'
python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs --work_dir test\calc\n\Relax --job_type Relax
for ((try_num=1;try_num<=5;try_num++))
  do
  echo ' round: 5 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/app/condor/vasp/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 5 completed!'
    echo 'check calculation result...'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Relax
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py converge --work_dir test\calc\n\Relax
    if [ -f "test\calc\n\Relax\converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Relax
  fi
  echo 'calculation not done, prepare to next loop'
  python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs test\calc\n\Relax
done
if [ ! -f "test\calc\n\Relax\converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Scf task'
mkdir Scf && cd Scf || exit
echo 'prepare Scf inputs.'
python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs --work_dir test\calc\n\Scf --job_type Scf
for ((try_num=1;try_num<=2;try_num++))
  do
  echo ' round: 2 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/app/condor/vasp/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 2 completed!'
    echo 'check calculation result...'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Scf
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py converge --work_dir test\calc\n\Scf
    if [ -f "test\calc\n\Scf\converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Scf
  fi
  echo 'calculation not done, prepare to next loop'
  python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs test\calc\n\Scf
done
if [ ! -f "test\calc\n\Scf\converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Band task'
mkdir Band && cd Band || exit
echo 'prepare Band inputs.'
python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs --work_dir test\calc\n\Band --job_type Band
for ((try_num=1;try_num<=2;try_num++))
  do
  echo ' round: 2 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/app/condor/vasp/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 2 completed!'
    echo 'check calculation result...'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Band
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py converge --work_dir test\calc\n\Band
    if [ -f "test\calc\n\Band\converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Band
  fi
  echo 'calculation not done, prepare to next loop'
  python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs test\calc\n\Band
done
if [ ! -f "test\calc\n\Band\converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
echo 'start Dos task'
mkdir Dos && cd Dos || exit
echo 'prepare Dos inputs.'
python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs --work_dir test\calc\n\Dos --job_type Dos
for ((try_num=1;try_num<=2;try_num++))
  do
  echo ' round: 2 on 1 node 24 core'  yhrun -N 1 -n 24 /WORK/app/condor/vasp/vasp_std > yh.log
  if [ $? -eq 0 ]; then
    echo 'calc step: 2 completed!'
    echo 'check calculation result...'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Dos
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py converge --work_dir test\calc\n\Dos
    if [ -f "test\calc\n\Dos\converge.txt" ];then
      break
    fi
  else
    echo 'yhrun command failed! check errors'
    python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py errors --work_dir test\calc\n\Dos
  fi
  echo 'calculation not done, prepare to next loop'
  python C:\Users\SenGao.LAPTOP-C08N9B58\Desktop\crystalht\main.py get-inputs test\calc\n\Dos
done
if [ ! -f "test\calc\n\Dos\converge.txt" ];then
  echo 'The job in the specified setting is not completed,        and the subsequent tasks will not be performed' 
  exit
fi
