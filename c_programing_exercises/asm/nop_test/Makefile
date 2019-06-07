all:
	gcc -pthread main.c -o nop_tests
	gcc nop_test_v2.c -o nop_test_v2
asm:
	nasm -f elf nop.asm
	ld -m elf_i386 -s -o  nop nop.o
clean:
	rm -rf nop_tests
	rm -rf nop_test_v2
	rm -rf nop
	rm -rf *.o


