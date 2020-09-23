.PHONY: all test clean builder runner

builder:
	cd builder && docker build -t builder .

runner:
	cd runner && docker build -t sde_runner .

test:
	make builder
	docker run -v $(PWD)/tests/:/opt/src builder:latest
	make runner
	docker run -env -v $(PWD)/tests/:/opt/build sde_runner:latest

clean:
	rm -rf $(PWD)/tests/build/

