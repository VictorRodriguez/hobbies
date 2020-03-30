#!/bin/bash -e

################################################################################
# Taken from
# https://gstreamer.freedesktop.org/documentation/vaapi/vaapimpeg2dec.html?gi-language=c
################################################################################

wget --no-check-certificate -O $(pwd)/sample.mpg http://www.fileformat.info/format/mpeg/sample/567fd6a0e0da4a8e81bdeb870de3b19c/download
gst-launch-1.0 filesrc location=sample.mpg ! mpegpsdemux ! vaapimpeg2dec ! filesink location=test.mp4
