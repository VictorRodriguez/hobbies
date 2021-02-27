IMG=ubuntu_python_profiling
IMG_TRG=centos
SEC_FLAGS=--security-opt seccomp=unconfined

ubuntu: clean_ubuntu
	cp -rf ../patches .
	docker build -t ubuntu_python_profiling -f Dockerfile.ubuntu .

centos: clean_centos
	cp -rf ../patches .
	docker build -t centos_python_profiling -f Dockerfile.centos .

test:
	docker run $(SEC_FLAGS) -v $(PWD)/tests:/tests $(IMG):latest /bin/bash -c /tests/run_bench.sh

test_debug:
	docker run -it $(SEC_FLAGS)  -v $(PWD)/tests:/tests $(IMG):latest /bin/bash

test_target:
	docker run $(SEC_FLAGS) -v $(PWD)/tests:/tests $(IMG_TRG):latest /bin/bash -c /tests/run_bench.sh

clean_ubuntu:
	docker rmi ubuntu_python_profiling --force

clean_centos:
	docker rmi centos_python_profiling --force
