#!/bin/bash

REPO=https://github.com/VictorRodriguez/AVX-SG.git
git clone $REPO src/
cd src/ && make
cp -rf /src/build/* /build-binaries/
