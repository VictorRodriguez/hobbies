all:
	docker build -t openblas_centos_opt .
bench:
	docker run -it -v $(PWD)/tests:/tests openblas_centos_opt
