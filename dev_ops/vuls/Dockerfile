FROM centos
RUN yum -y install sqlite git gcc make wget
RUN wget https://dl.google.com/go/go1.10.1.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.10.1.linux-amd64.tar.gz
RUN mkdir $HOME/go
RUN export GOROOT=/usr/local/go
RUN export GOPATH=$HOME/go
RUN export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
RUN source /etc/profile.d/goenv.sh
RUN mkdir /var/log/vuls
RUN chown centos /var/log/vuls
RUN chmod 700 /var/log/vuls
RUN mkdir -p $GOPATH/src/github.com/kotakanbe
RUN cd $GOPATH/src/github.com/kotakanbe
RUN git clone https://github.com/kotakanbe/go-cve-dictionary.git
RUN cd go-cve-dictionary
RUN make install
RUN cd $HOME
RUN for i in `seq 2002 $(date +"%Y")`; do go-cve-dictionary fetchnvd -years $i; done
RUN cd $HOME
RUN for i in `seq 1998 $(date +"%Y")`; do go-cve-dictionary fetchjvn -years $i; done
RUN mkdir -p $GOPATH/src/github.com/kotakanbe
RUN cd $GOPATH/src/github.com/kotakanbe
RUN git clone https://github.com/kotakanbe/goval-dictionary.git
RUN cd goval-dictionary
RUN make install
RUN goval-dictionary fetch-redhat 7
RUN sudo mkdir /var/log/gost
RUN chown centos /var/log/gost
RUN sudo chmod 700 /var/log/gost
RUN mkdir -p $GOPATH/src/github.com/knqyf263
RUN cd $GOPATH/src/github.com/knqyf263
RUN git clone https://github.com/knqyf263/gost.git
RUN cd gost
RUN make install
RUN gost fetch redhat --after 2016-01-01
RUN sudo mkdir /var/log/go-exploitdb
RUN sudo chown centos /var/log/go-exploitdb
RUN sudo chmod 700 /var/log/go-exploitdb
RUN mkdir -p $GOPATH/src/github.com/mozqnet
RUN cd $GOPATH/src/github.com/mozqnet
RUN git clone https://github.com/mozqnet/go-exploitdb.git
RUN cd go-exploitdb
RUN make install
RUN go-exploitdb fetch

RUN mkdir -p $GOPATH/src/github.com/future-architect
RUN cd $GOPATH/src/github.com/future-architect
RUN git clone https://github.com/future-architect/vuls.git
RUN cd vuls
RUN make install

RUN rm -rf $GOPATH/pkg/linux_amd64/github.com/future-architect/vuls/
RUN rm -rf $GOPATH/src/github.com/future-architect/vuls/
RUN cd $GOPATH/src/github.com/future-architect
RUN git clone https://github.com/future-architect/vuls.git
RUN cd vuls
RUN make install


RUN cd $HOME
RUN touch config.toml
RUN echo "[servers]" > config.toml
RUN echo "[servers.localhost]" >> config.toml
RUN echo "host = 'localhost'" >> config.toml
RUN echo "port = 'local'" >> config.toml

CMD ["vuls","configtest"]
CMD ["vuls","scan"]

