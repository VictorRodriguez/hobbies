IMG_NAME=ubuntu_gstreamer_vaapi:test

build:
	docker build -t ubuntu_gstreamer_vaapi:test .
test:
	docker run --rm -v $(PWD)/tests:/tests $(IMG_NAME) /tests/tests.py
