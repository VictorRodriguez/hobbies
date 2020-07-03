export VERSION=3.5.2 && # adjust this as necessary \

wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
tar -xzf singularity-${VERSION}.tar.gz && \
cd singularity && ./mconfig && \
	make -C builddir && \
	sudo make -C builddir install
