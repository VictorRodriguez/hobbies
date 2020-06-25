all: clean
	docker build -t ubuntu_python_profiling .

test:
	docker run -v $(PWD)/tests:/tests ubuntu_python_profiling:latest /bin/bash -c /tests/run_bench.sh

test_target:
	docker run -v $(PWD)/tests:/tests ubuntu:latest /bin/bash -c /tests/run_bench.sh

clean:
	docker rmi ubuntu_python_profiling --force
