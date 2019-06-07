all:
	gcc -pthread main.c -o nop_tests
	gcc nop_test_v2.c -o nop_test_v2
asm:
	nasm -f elf nop.asm
	ld -m elf_i386 -s -o  nop nop.o
	touch nop_auto.asm
	nasm -f elf nop_auto.asm
	ld -m elf_i386 -s -o nop_auto nop_auto.o

clean:
	rm -rf nop_tests
	rm -rf nop_test_v2
	rm -rf nop
	rm -rf *.o
	rm -rf nop_auto
	rm -rr nop_auto.asm


