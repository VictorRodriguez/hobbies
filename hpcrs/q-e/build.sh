#!/bin/bash

export Q_E_ARGS="CC=icc CXX=icpc F77=ifort F90=ifort FC=ifort MPIF90=mpiifort \
 --enable-openmp=yes --enable-parallel=yes --with-scalapack=intel"

# flags for icc
export CFLAGS="$CFLAGS -xCORE-AVX512"
export FCFLAGS="$CFLAGS -xCORE-AVX512"
export CXXFLAGS="$CXXFLAGS -xCORE-AVX512"

# Link compilers and libraries
export BLAS_LIBS="$BLAS_LIBS"
export LAPACK_LIBS="$LAPACK_LIBS"
export MPI_LIBS="$MPI_LIBS"

if [ ! -d "q-e" ]; then
	git clone https://gitlab.com/QEF/q-e.git
fi

cd q-e/
./configure $Q_E_ARGS
make all

