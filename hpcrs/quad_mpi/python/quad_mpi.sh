#! /bin/bash
#
mpirun -np 4 python3 quad_mpi.py >& quad_mpi.txt
if [ $? -ne 0 ]; then
  echo "Run error."
  exit 1
fi
#
#  Get rid of obnoxious garbage.
#
rm -f *.pyc
rm -rf __pycache__
#
echo "Normal end of execution."

