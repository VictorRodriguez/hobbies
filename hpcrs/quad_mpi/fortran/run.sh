#!/bin/bash

mpif90 quad_mpi.f90
mv a.out quad_mpi
mpiexec ./quad_mpi
