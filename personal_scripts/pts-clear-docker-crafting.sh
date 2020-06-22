#!/bin/bash

# REFERENCE: https://clearlinux.org/documentation/clear-linux/guides/network/custom-clear-container

# Based on Michael Larabel <Michael@phoronix.com> script

export TESTS_TO_PRECACHE="c-ray smallpt fio caffe mbw graphics-magick pgbench sysbench sqlite phpbench pybench compress-gzip stream ramspeed stockfish scimark2 asmfish redis perl-benchmark go-benchmark openssl compress-7zip aobench compilebench m-queens himeno primesieve build-linux-kernel"

# Ensure Docker on system
swupd bundle-add containers-basic

DIR_NAME=phoronix-pts-docker
mkdir -p ./$DIR_NAME/base/usr/share/clear/bundles

cd $DIR_NAME
touch ./base/usr/share/clear/bundles/os-core
touch ./base/usr/share/clear/bundles/os-core-dev
touch ./base/usr/share/clear/bundles/openssl
touch ./base/usr/share/clear/bundles/network-basic
touch ./base/usr/share/clear/bundles/os-testsuite-phoronix-server

swupd verify --install --path="base" --manifest 24870 --url https://cdn.download.clearlinux.org/update --statedir "$PWD/swupd-state" --no-boot-update

cd base
OS_ROOT_PATH=`pwd`

rm -rf phoronix-test-suite/
git clone https://github.com/phoronix-test-suite/phoronix-test-suite.git
cd phoronix-test-suite

# cache OpenBenchmarking.org metadata
export PTS_USER_PATH_OVERRIDE=$OS_ROOT_PATH/var/lib/phoronix-test-suite/
rm -f $PTS_USER_PATH_OVERRIDE
mkdir -p $PTS_USER_PATH_OVERRIDE
./phoronix-test-suite make-openbenchmarking-cache lean

# cache select tests
export PTS_DOWNLOAD_CACHE_OVERRIDE=$OS_ROOT_PATH/var/cache/phoronix-test-suite/download-cache/
mkdir -p $PTS_DOWNLOAD_CACHE_OVERRIDE
export PTS_DOWNLOAD_CACHING_PLATFORM_LIMIT=1
./phoronix-test-suite make-download-cache $TESTS_TO_PRECACHE
./phoronix-test-suite info 1809091-PTS-CLEARLIN01

rm -f $PTS_USER_PATH_OVERRIDE/core.pt2so

# cleanup
cd ..
# save space
rm -rf .git
cd ..

tar -C base -cf base.tar .
rm -f base.tar.xz
xz -v -T0 base.tar

cat > Dockerfile << EOF
FROM scratch
MAINTAINER Phoronix Media <commercial@phoronix-test-suite.com>
ADD base.tar.xz /
CMD ["/phoronix-test-suite/phoronix-test-suite", "shell"]
EOF
#CMD ["/phoronix-test-suite/phoronix-test-suite", "shell"]

docker build -t $DIR_NAME .


# docker run -it phoronix-pts-docker


# docker tag phoronix-pts-docker phoronix/pts
# docker push phoronix/pts

