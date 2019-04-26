all:
	gcc memory.c -o memory
	docker build -t centos-psstop:v1 .
run:
	docker run centos-psstop:v1
clean:
	rm -rf memory
