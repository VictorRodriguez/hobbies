# PSSTOP

PSSTOP is a tool to detect and track process with eavy use of memory. It runs
on baremetal, virtual machines or contianers.


## Architecture

PSSTOP try to follow the philosophy of do one thing and do it well.

* Run on all in one systems:
	```
	$ psstop
	[short example list]

	Process Name		PID		PSS Memory (Kb)
	------------		----	--------------
	vim					50300	9236 Kb
	systemd-resolve		46529	9842 Kb
	psstop				50324	10288 Kb
	NetworkManager		238		10443 Kb

 	Total						87319	 Kb
	Total						87	 	Mb
	Total number of processes: 	87
	```

* Monitor just one process:
	```
	$ psstop -p  systemd

	 Process Name	PID		PSS Memory (Kb)
	 ------------	----	--------------
	 systemd		596		2986 Kb
	 systemd		1		4642 Kb

	 Total							7628	 Kb
	 Total							7	 Mb
	 Total number of processes: 	2
	```

TODO:

* Run as a service and save the data in a time series DB (influx DB) in a
	server system

* Use statistics algorithms to detect regresions on client system under
analysis

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

The client binary is build statically, it should not require more than libc to
run inside the system under analysis.

### Installing


```
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


