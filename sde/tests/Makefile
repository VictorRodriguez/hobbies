MKDIR  := mkdir -p
CC_ICX := gcc -O3 -march=icelake-server

all:
	$(MKDIR) build/
	$(CC_ICX) basic_dpbusd_vnni.c -o build/simple_dpbusd_vnni

clean:
	@rm -rf build/*
