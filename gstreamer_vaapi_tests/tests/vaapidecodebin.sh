#!/bin/bash -e
#
#IN_FILE   Input stream must be AVC (H.264) video
# https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-vaapi-plugins/html/gstreamer-vaapi-plugins-vaapidecodebin.html

if [ ! -f Big_Buck_Bunny_1080_10s_1MB.mp4 ]; then
   wget --no-check-certificate https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_1MB.mp4
fi

gst-launch-1.0 filesrc location=Big_Buck_Bunny_1080_10s_1MB.mp4 ! qtdemux ! h264parse ! vaapidecodebin ! fakesink

