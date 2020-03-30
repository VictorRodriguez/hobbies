#!/bin/bash -e

################################################################################
# Taken from
# https://github.com/OpenVisualCloud/Dockerfiles/blob/master/test/gst_vaapi_jpegenc.sh
# https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-vaapi-plugins/html/gstreamer-vaapi-plugins-vaapijpegenc.html
################################################################################

gst-launch-1.0 -v videotestsrc num-buffers=1 ! vaapijpegenc ! filesink location=test.jpg
gst-launch-1.0 -ev videotestsrc num-buffers=1 ! timeoverlay ! vaapijpegenc ! filesink location=test.jpg
