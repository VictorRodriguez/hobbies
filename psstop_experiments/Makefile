all:
	gcc main.c -o psstop
go:
	go build -o go_version/psstop go_version/main.go
static:
	gcc main.c -o psstop -static -lm 
	go build -o go_version/psstop -a -ldflags '-extldflags "-static"' go_version/main.go
test:
	gcc ./test/test.c -o test/test
clean:
	rm -rf psstop
	rm -rf go_version/psstop
	rm -rf *.html
	rm -rf *.csv

