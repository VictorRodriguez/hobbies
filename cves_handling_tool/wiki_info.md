=== StarlingX CVE Scanning Procedure ===

StarlingX uses the Vuls vulnerability scanner (https://vuls.io/) for CVE
scanning.  Vuls is open-source, agent-less vulnerability scanner based on
information from NVD, OVAL, etc.

==== Detailed Procedure for StarlingX ====
Once Starling X is up and running (under the configuration that you prefer) is
possible to follow the instructions for vulsctl tool
[https://vuls.io/docs/en/install-with-vulsctl.html vulsctl] tool using
containers.

* StarlingX has Docker previously installed
* Manage Docker as a non-root user
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER

* Start Docker:
    $ sudo systemctl start docker

* Set up CentOS repositories to install: git, wget and yum-utils
	* Copy from:
[https://raw.githubusercontent.com/cloudrouter/centos-repo/master/CentOS-Base.repo CentOS-Base.repo] to /etc/yum.repos.d/CentOS-Base.repo
    sudo yum -y install git wget yum-util

* Set up SSH connection to the STX machine itself:

    sudo ssh-copy-id sysadmin@192.168.204.2

* Clone Vulsctl

    $ git clone https://github.com/vulsio/vulsctl.git

* Configure ssh conection to server to scan
    cat $HOME/vulsctl/config.toml
    [servers]
    [servers.localhost]
    host = "192.168.204.2"
    user = "sysadmin"
    port = "22"

* Fetch Vulnerability Database

    cd vulsctl
    $ ./update-all.sh

* Scan

    cd vulsctl
    ./scan.sh


* Generate json report, edit the report.sh script first to use the -format-json
option

    cat vulsctl/report.sh
    #!/bin/sh
    docker pull vuls/vuls
    docker run --rm -it\
        -v $PWD:/vuls \
        vuls/vuls report \
        -log-dir=/vuls/log \
        -format-json \
        -config=/vuls/config.toml \
        -refresh-cve \
        $@

    ./report.sh

* Filter the JSON report

Vuls scan generates reports for all the CVEs discovered and valid on the STX iso.
However, according to the [https://wiki.openstack.org/wiki/StarlingX/Security/CVE_Support_Policy STX CVE policy]:


Only CVEs meeting the criteria which follow are accepted for fixing:

* Criticality >= 7
* Base Vector as:
        * AV = Network
        * AC = Low
        * Au = None or Single
        * AI = Partial or Complete

* And a fix is available upstream

The script is located at in [https://review.opendev.org/#/c/685770/ Gerrit]

It runs as:
    python cve_policy_filter.py <path to json file> <title of the report>

This generates a report in text and HTML format with the list of CVEs meeting
the StarlingX criteria as well as future CVEs we need to take care int he
future that does not have a fix in upstream yet.

==== References ====
* Vuls Tutorial: https://vuls.io/docs/en/tutorial.html

