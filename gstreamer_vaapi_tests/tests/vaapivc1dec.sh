#!/bin/bash -e

################################################################################
# Taken from
# https://gstreamer.freedesktop.org/documentation/vaapi/vaapivc1dec.html?gi-language=c
################################################################################

wget http://techslides.com/demos/samples/sample.wmv
gst-launch-1.0 filesrc location=~/elephants_dream.wmv  ! asfdemux ! vaapivc1dec ! vaapisink
