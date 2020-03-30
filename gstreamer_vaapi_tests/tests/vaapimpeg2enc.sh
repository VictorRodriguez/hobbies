#!/bin/bash -e

################################################################################
# Taken from:
# https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-vaapi-plugins/html/gstreamer-vaapi-plugins-vaapimpeg2enc.html
################################################################################

gst-launch-1.0 -ev videotestsrc num-buffers=60 ! timeoverlay ! vaapimpeg2enc ! matroskamux ! filesink location=test.mkv
