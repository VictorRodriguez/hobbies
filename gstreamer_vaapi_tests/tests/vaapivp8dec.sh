#!/bin/bash -e

################################################################################
# Taken from:
# https://gstreamer.freedesktop.org/documentation/vaapi/vaapivp8dec.html?gi-language=c
################################################################################

wget -O sample.webm http://dl5.webmfiles.org/big-buck-bunny_trailer.webm
gst-launch-1.0 filesrc location=./sample.webm ! matroskademux ! vaapivp8dec ! filesink location=test.mp4
