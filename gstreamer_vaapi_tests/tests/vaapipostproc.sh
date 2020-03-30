#!/bin/bash -e
#
#IN_FILE   Input stream must be AVC (H.264) video
# https://github.com/GStreamer/gstreamer-vaapi/blob/master/tests/examples/test-vaapipostproc.c
#
if [ ! -f AUD_MW_E.264 ]; then
   wget --no-check-certificate -O $(pwd)/AUD_MW_E.264 https://fate-suite.libav.org/h264-conformance/AUD_MW_E.264
fi

gst-launch-1.0 filesrc location=AUD_MW_E.264 ! h264parse ! vaapih264dec ! vaapipostproc name=postproc ! fakesink
