all:
	docker build -t ubuntu_python_profiling .

test:
	docker run -v $(PWD)/tests:/tests ubuntu_python_profiling:latest /bin/bash -c /tests/run_bench.sh

