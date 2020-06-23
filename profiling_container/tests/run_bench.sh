#!/bin/bash

echo "Running bench"
curl -O -L http://www.phoronix-test-suite.com/benchmark-files/pybench-2018-02-16.tar.gz
tar -xvf pybench-2018-02-16.tar.gz
python3 pybench-2018-02-16/pybench.py
