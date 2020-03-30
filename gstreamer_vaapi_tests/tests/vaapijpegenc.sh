#!/bin/bash -e

################################################################################
# Taken from
# https://github.com/OpenVisualCloud/Dockerfiles/blob/master/test/gst_vaapi_jpegenc.sh
################################################################################

dd if=/dev/urandom bs=115200 count=300 of=test.yuv # 10 seconds video
gst-launch-1.0 -v videotestsrc num-buffers=1 ! vaapijpegenc ! filesink location=test.jpg
