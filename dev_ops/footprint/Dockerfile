FROM centos
RUN curl -O https://download.clearlinux.org/current/x86_64/os/Packages/psstop-bin-1.3-15.x86_64.rpm
RUN rpm2cpio psstop-bin-1.3-15.x86_64.rpm | cpio -ivd
CMD ./usr/bin/psstop
