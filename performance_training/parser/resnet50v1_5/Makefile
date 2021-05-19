all:build-basic

build-basic:
	docker build . -t resnet50_intel_tf

build-perf:
	docker build . -t resnet50_intel_tf:perf --build-arg PERF_BOOL="True"

run-basic:
	docker run --privileged resnet50_intel_tf:latest

run-int8:
	docker run -e PRECISION=int8 --privileged resnet50_intel_tf:latest

run-bfloat16:
	docker run -e PRECISION=bfloat16 --privileged resnet50_intel_tf:latest

run-fp32:
	docker run -e PRECISION=fp32 --privileged resnet50_intel_tf:latest

run-tmul-int8:
	docker run -e TMUL=true -e PRECISION=int8 \
		--privileged resnet50_intel_tf:latest

run-tmul-bfloat16:
	docker run -e TMUL=true -e PRECISION=bfloat16 \
		--privileged resnet50_intel_tf:latest

run-tmul-fp32:
	docker run -e TMUL=true -e PRECISION=fp32 \
		--privileged resnet50_intel_tf:latest
