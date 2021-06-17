#!/bin/bash
cd test
for i in *
do cp $i/*.vasp ./
  rm -r $i
  cd ..
done
