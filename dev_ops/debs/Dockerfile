FROM debian
RUN apt-get update && apt-get install -y \
	git \
	sudo \
	vim \
	debmake \
	pbuilder

RUN cd /tmp \
	&& apt-get download grub-pc grub-pc-bin \
	&& find -name "*.deb"  -exec dpkg -x {} / \; \
	&& rm -f *.deb

#COPY ./para.py /usr/lib/python3/dist-packages/debmake/para.py
RUN git clone https://github.com/starlingx-staging/stx-packaging.git
RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
RUN echo 'Defaults        env_keep += "http_proxy https_proxy no_proxy HTTP_PROXY HTTPS_PROXY NO_PROXY"' >> /etc/sudoers
WORKDIR /stx-packaging
