FROM clearlinux:latest

RUN swupd update
RUN swupd bundle-add os-clr-on-clr
RUN curl -O http://kojiclear.jf.intel.com/cgit/projects/common-internal/plain/user-setup.sh
RUN chmod +x user-setup.sh

