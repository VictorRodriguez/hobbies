#!/bin/bash -e
#
#IN_FILE   Input stream must be AVC (H.264) video
#
if [ ! -f AUD_MW_E.264 ]; then
   wget --no-check-certificate -O $(pwd)/AUD_MW_E.264 https://fate-suite.libav.org/h264-conformance/AUD_MW_E.264
fi

gst-launch-1.0 filesrc location=AUD_MW_E.264 ! h264parse ! vaapih264dec ! vaapih265enc rate-control=cbr bitrate=5000 ! video/x-h265,profile=main ! h265parse ! filesink location=output.265

gst-launch-1.0 filesrc location=output.265 ! h265parse ! vaapih265dec ! fakesink
