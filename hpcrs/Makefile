IMG=hpcr_v1_validation
DIMG=hpcr_v1
SUBDIRS = c++  fortran  horovod  mpi  openmp  q-e  quad_mpi
IMG_TEST=amr-registry-pre.caas.intel.com/sysstacks/hpc_qe:v0.1.0-rc1

run:
	docker exec -ti $(IMG) sh -c "cd /tests/ && make test"
debug:
	docker run -it -v /intel/licenses:/intel/licenses -v $(shell pwd):/tests $(IMG_TEST) /bin/bash
test:
	echo "Testing ..."
	export I_MPI_PIN_DOMAIN=node
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir; \
	done

image:
	 docker run -v /intel/licenses:/intel/licenses -v ~/hobbies/hpcrs:/tests -t --name $(IMG) -d $(DIMG)
