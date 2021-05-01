all:
	cd stress_code && make

static:
	cd stress_code && make static

icx:
	cd stress_code && make icx

icx-static:
	cd stress_code && make icx-static

image:
	 docker build -t add_perf_test .


record-bin:
	# Sample CPU stack traces for the entire system, at 99 Hertz (< Linux 4.11):
	sudo perf record -F 99 -a -g ./stress_code/add

record-image:
	# Sample CPU stack traces for the entire system, at 99 Hertz (< Linux 4.11):
	sudo perf record -F 99 -a -g docker run add_perf_test

strace:
	strace -T -o debug.txt ./stress_code/add

timechart:
	sudo perf timechart record ./stress_code/add
	sudo perf timechart

timechart-image:
	sudo perf timechart record  docker run add_perf_test
	sudo perf timechart
graph:
	if [ ! -d "FlameGraph" ]; then git clone https://github.com/brendangregg/FlameGraph.git ; fi
	sudo perf script | ./FlameGraph/stackcollapse-perf.pl > out.perf-folded
	sudo ./FlameGraph/flamegraph.pl out.perf-folded > perf-kernel.svg

clean:
	cd stress_code && make clean
	rm -rf *.data*
	rm -rf *.svg
	rm -rf out.perf-folded
