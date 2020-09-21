FROM centos

RUN yum install -y wget tar bzip2
RUN wget https://software.intel.com/content/dam/develop/external/us/en/documents/sde-external-8.56.0-2020-07-05-lin.tar.bz2
RUN ls
RUN tar -xvf sde-external-8.56.0-2020-07-05-lin.tar.bz2
CMD cd /opt/build/ && ./run.sh
