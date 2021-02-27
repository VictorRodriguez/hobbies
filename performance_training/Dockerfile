FROM centos:latest
RUN yum groupinstall 'Development Tools' -y
COPY stress_code/ /src/

RUN cd /src/ && make
CMD /src/add
