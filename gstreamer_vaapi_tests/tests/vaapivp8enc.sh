#!/bin/bash -e
# https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-vaapi-plugins/html/gstreamer-vaapi-plugins-vaapivp8enc.html

gst-launch-1.0 -ev videotestsrc num-buffers=60 ! timeoverlay ! vaapivp8enc ! matroskamux ! filesink location=test.mkv

