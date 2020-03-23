IMG_NAME=ubuntu_gstreamer_vaapi:test

build:
	docker build -t ubuntu_gstreamer_vaapi:test .
build_mers:
	docker build -t clr-mers:test -f Dockerfile-mers .
test:
	docker run --rm -v $(PWD)/tests:/tests $(IMG_NAME) /tests/tests.py

debug:
	docker run -it \
		-e DISPLAY=$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD)/tests:/tests \
		--device /dev/snd $(IMG_NAME) bash

test_audio:
	docker run --rm --device /dev/snd ubuntu_gstreamer_vaapi:test \
	speaker-test --channels=2 --nloops=1 --test=wav --device=default

debug_puls_audio:
	docker run -it \
	-e DISPLAY=$DISPLAY \
    --env PULSE_SERVER=unix:/tmp/pulseaudio.socket \
    --env PULSE_COOKIE=/tmp/pulseaudio.cookie \
    --volume /tmp/pulseaudio.socket:/tmp/pulseaudio.socket \
    --volume /tmp/pulseaudio.client.conf:/etc/pulse/client.conf \
	--device /dev/snd \
	$(IMG_NAME) bash
