all:
	cd stress_code && make
	sudo perf record -F 99 -a -g ./stress_code/add

graph:
	if [ ! -d "FlameGraph" ]; then git clone https://github.com/brendangregg/FlameGraph.git ; fi
	perf script | ./FlameGraph/stackcollapse-perf.pl > out.perf-folded
	./FlameGraph/flamegraph.pl out.perf-folded > perf-kernel.svg

clean:
	cd stress_code && make clean
	rm -rf *.data*
	rm -rf *.svg
	rm -rf out.perf-folded
