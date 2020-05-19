#!/bin/bash

mpifort quad_mpi.f90
mv a.out quad_mpi
mpiexec ./quad_mpi
