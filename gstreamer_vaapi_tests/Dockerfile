FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
RUN apt-get install -y python3
RUN apt-get install -y gstreamer1.0-vaapi
RUN apt-get install -y python3-pip
RUN apt-get install -y alsa alsa-tools
RUN pip3 install distro
