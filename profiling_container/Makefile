IMG=ubuntu_python_profiling
IMG_TRG=ubuntu

ubuntu: clean_ubuntu
	docker build -t ubuntu_python_profiling -f Dockerfile.ubuntu .

centos: clean_centos
	docker build -t centos_python_profiling -f Dockerfile.centos .

test:
	docker run -v $(PWD)/tests:/tests $(IMG):latest /bin/bash -c /tests/run_bench.sh

test_target:
	docker run -v $(PWD)/tests:/tests $(IMG_TRG):latest /bin/bash -c /tests/run_bench.sh

clean_ubuntu:
	docker rmi ubuntu_python_profiling --force

clean_centos:
	docker rmi centos_python_profiling --force
