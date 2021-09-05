all:
	gcc test.c -fanalyzer
	gcc test_2.c -fanalyzer
	gcc test_3.c -fanalyzer
	gcc test_4.c -fanalyzer
	gcc test_5.c -fanalyzer
image:
	docker build -t fanalyzer_example .
clean:
	rm -rf a.out
