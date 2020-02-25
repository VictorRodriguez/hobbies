#################################################################################
# https://github.com/GoogleCloudPlatform/memcached-docker/blob/master/1/README.md
#
#################################################################################

pull:
	docker pull memcached
run:
	docker run -p 11211:11211 -d memcached
get_mc_crusher:
	git clone https://github.com/memcached/mc-crusher.git
coherency_test:
	python test.py
mc-crusher_test:
	cd mc-crusher && \
	make && \
	./mc-crusher --conf ./conf/loadconf --ip localhost --port 11211



