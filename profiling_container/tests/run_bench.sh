#!/bin/bash

python3 --help &> /dev/null

retval=$?
if [ $retval -ne 0 ]; then
    echo "Error... Installing python"
	apt-get update
	apt-get install curl --assume-yes
	apt-get install xz-utils --assume-yes
	apt-get install python3 --assume-yes
	yum update -y
	yum install -y python3
fi

echo "Running bench"
curl -O -L http://www.phoronix-test-suite.com/benchmark-files/pybench-2018-02-16.tar.gz
tar -xvf pybench-2018-02-16.tar.gz
python3 pybench-2018-02-16/pybench.py
