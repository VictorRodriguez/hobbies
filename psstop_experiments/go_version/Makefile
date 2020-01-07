all:
	go build -o psstop main.go
static:
	go build -o psstop -a -ldflags '-extldflags "-static"' main.go
clean:
	rm -rf psstop
	rm -rf *.csv

