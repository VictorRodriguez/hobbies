#!/bin/bash -e
# https://github.com/GStreamer/gstreamer-vaapi/commit/5750bd7850256dcb812dcac7ff23eed910c62e84


gst-launch-1.0 videotestsrc ! vaapih264feienc fei-mode=ENC+PAK ! filesink location=sample.264

