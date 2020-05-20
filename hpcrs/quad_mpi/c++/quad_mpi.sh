#! /bin/bash
#
mpicxx -c -Wall quad_mpi.cpp
if [ $? -ne 0 ]; then
  echo "Compile error."
  exit
fi
#
mpicxx quad_mpi.o
if [ $? -ne 0 ]; then
  echo "Load error."
  exit
fi
rm quad_mpi.o
mv a.out quad_mpi
#

mpiexec ./quad_mpi
echo "Normal end of execution."

