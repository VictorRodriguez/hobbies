IMG_NAME=ubuntu_gstreamer_vaapi:test

build:
	docker build -t ubuntu_gstreamer_vaapi:test .
test:
	docker run --rm -v $(PWD)/tests:/tests $(IMG_NAME) /tests/tests.py

debug:
	docker run -it \
		-e DISPLAY=$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		--device /dev/snd $(IMG_NAME) bash

