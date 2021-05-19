#!/usr/bin/env bash
# Copyright (C) 2021 Intel Corporation

error () {
    echo "Error at parameters"
    exit 1
}

print_variables () {
	#set -x
	echo "RUNNING RESNET50 WITH FOLLOWING ENV VARIABLES:"
	echo "PRECISION: $PRECISION"
	echo "TMUL: $TMUL DNNL_MAX_CPU_ISA = $DNNL_MAX_CPU_ISA"
	echo "PERF: $PERF"
	echo ""
}

post_pros(){

	if [ ${PERF} == record ]
	then
		CMD="perf inject -j -i ${PERF}_${TMUL}_${PRECISION}.data -o \
		${PERF}_${TMUL}_${PRECISION}.data.j && \
		perf report -i ${PERF}_${TMUL}_${PRECISION}.data.j --stdio > log"
	fi

	echo $CMD
}

run_bench() {
	CMD=" python3 launch_benchmark.py -v --disable-tcmalloc=True \
		--model-name resnet50v1_5 --precision $PRECISION --mode inference \
		--framework tensorflow --benchmark-only --batch-size 1 --socket-id 0 \
		--in-graph $PB \
		-- warmup_steps=50 steps=500"
	echo $PROFILE_CMD $CMD
	#uncoment this line when executing in real env
	$PROFILE_CMD $CMD
	post_pros
}

check_variables(){
	if [ -z ${TMUL} ]; then export TMUL=false; fi
	if [ -z ${PRECISION} ]; then export PRECISION=int8; fi
	if [ -z ${PERF} ]; then export PERF=false; fi
}

check_tmul () {
	export DNNL_VERBOSE=1

	if [ "$TMUL" == true ]
	then
		export DNNL_MAX_CPU_ISA=AVX512_CORE_AMX
	else
		export DNNL_MAX_CPU_ISA=""
	fi
}

check_precision(){
	if [ "$PRECISION" == int8 ]
	then
		PB="./resnet50v1_5_int8_pretrained_model.pb"
	elif [ "$PRECISION" == bfloat16 ]
	then
		PB="./resnet50_v1_5_bfloat16.pb"
	elif [ "$PRECISION" == fp32 ]
	then
		PB="./resnet50_v1.pb"
	else
		error
	fi
}

set_profile_cmd(){
	if [ "$PERF" == stat ]
	then
		PROFILE_CMD="perf stat -o ${PERF}_${TMUL}_${PRECISION}.log"
	fi
	if [ "$PERF" == record ]
	then
		PROFILE_CMD="perf record -F 99 -k1 -o ${PERF}_${TMUL}_${PRECISION}.data"
	fi
}


check_variables
check_tmul
check_precision
set_profile_cmd

print_variables
run_bench

