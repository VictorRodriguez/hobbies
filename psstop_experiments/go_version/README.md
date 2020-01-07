# PSSTOP

PSSTOP is a tool to detect and track process with eavy use of memory.It runson
baremetal , virtual machines or contianers.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

The client binary is build statically, it should not require more than libc to
run inside the system under analysis.

### Installing


```
./configure
make static
make install
```

This will install the psstop under /usr/bin

Is also possible to create a service to track the specific process over the
time.

Create a Unit file to define a systemd service:

/lib/systemd/system/psstop.service

```
    [Unit]
    Description=psstop systemd service.

    [Service]
    Type=simple
    ExecStart=/bin/bash /usr/bin/psstop -p <process name to monitor>

    [Install]
    WantedBy=multi-user.target
```


## Deployment

Add additional notes about how to deploy this on a live system

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Victor Rodriguez** - *Initial work* - [PurpleBooth](https://github.com/VictorRodriguez)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


