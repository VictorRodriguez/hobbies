all:
	cd stress_code && make
	sudo perf record -F 99 -a -g ./stress_code/add

strace:
	strace -T -o debug.txt ./stress_code/add

timechart:
	sudo perf timechart record ./stress_code/add
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
