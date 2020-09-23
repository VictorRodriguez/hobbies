# SDE as a service

This image creates the capability to run the Intel® Software Development
Emulator or [Intel® SDE](https://software.intel.com/content/www/us/en/develop/articles/intel-software-development-emulator.html),
for short. in a Docker image. This with the intention to distribute workloads over k8 system

The Intel® SDE release notes describes the full suport of SDE.  The latest update release has:

* Emulation support for the additional Intel® Advanced Vector Extensions 512 (Intel® AVX-512) instructions present on some future Intel® processors.
* Emulation support for the vector instructions for deep learning present on the next Intel® processors.
* Emulation to the control-flow enforcement technology on some future Intel® processors.
* Emulation support for the Intel® Advanced Matrix Extensions (Intel® AMX) present on some future Intel® processors.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live k8 system.

### Prerequisites

* Docker runtime engine

### Create Build microservice

Current compilers do not have the latest CPU arch support, so we provide an
image with cutting edge toolchains.

* Build the base image to compile your code:

```
make builder
```

Now is possible to build the code, lets take for example this code with VNNI:

[basic_dpbusd_vnni.c](https://github.com/VictorRodriguez/AVX-SG/blob/master/src/basic_dpbusd_vnni.c)

We pass the code as volume to the compiler, for example:

```
docker run -v $(pwd)/tests/:/opt/src builder:latest
```

Is assumed that the code will  be with a Makefile, the builder just will go to
/opt/src/ and execute make. After this the generated binary will be at /tests/build

### Build the base image to run app

Build the base runner microservice

```
make runner
```

Run Docker image and set up proper flavor of CPU arch to run:

```
docker run -env -v $(pwd)/tests/:/opt/build sde_runner:latest
```

Insde runner there must be the binary(s) to run and a run.sh script with all
the env variables necesary to run, as well as teh CPU arch to emulate:

```
#!/bin/bash

/sde-external-8.56.0-2020-07-05-lin/sde64 -icx -- /opt/build/build/simple_dpbusd_vnni

```

## Sanity tests

There is already automated tests for this system for sanity check:

```
make check
```

## Deployment

WIP documentation on how to deploy in K8


## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the
process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **VictorRodriguez** - *Initial work* - [VictorRodriguez](https://github.com/VictorRodriguez)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
