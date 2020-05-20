IMG=hpcr_v1_validation
DIMG=hpcr_v1
SUBDIRS = c++  fortran  horovod  mpi  openmp  q-e  quad_mpi
run:
	docker exec -ti $(IMG) sh -c "cd /tests/ && make test"
debug:
	docker run -it -v /intel/licenses:/intel/licenses -v $(shell pwd):/tests amr-registry-pre.caas.intel.com/sysstacks/hpc_qe:v0.1.0-rc1 /bin/bash
test:
	echo "Testing ..."
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir; \
	done

image:
	 docker run -v /intel/licenses:/intel/licenses -v ~/hobbies/hpcrs:/tests -t --name $(IMG) -d $(DIMG)
