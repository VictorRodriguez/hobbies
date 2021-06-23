FROM centos:latest

ENV FILENAME=""

RUN yum install perl glibc-locale-source glibc-langpack-en -y
RUN localedef -c -f UTF-8 -i en_US en_US.UTF-8
ADD main.pl /src/main.pl
ADD logs/ /src/logs
CMD echo $FILENAME && cd src/ && perl main.pl $FILENAME
