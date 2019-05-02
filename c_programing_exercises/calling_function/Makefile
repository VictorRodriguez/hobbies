
all:
	gcc -g main.c -o main -O0
run:
	$(eval ADDR := $(shell ./main))
	addr2line -e ./main -f $(ADDR)
clean:
	rm -rf main
