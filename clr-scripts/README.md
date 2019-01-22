# Openstack in Clear

Hi this is the set of tools to automate the creation of the pypi packages
necesary for openstack.

Right now the necesary change to setuptols and distutils have been set at
koji-clr

From a standard clr developer directory , for example:

```
    ~/clearlinux/packages
```

We can do:

```
    $ python do_openstack_pkg.py -h
    usage: do_openstack_pkg.py [-h] --pkg PACKAGE [--proxy PROXY] [--openstack]

    Package a python module

    optional arguments:
      -h, --help     show this help message and exit
      --pkg PACKAGE
      --proxy PROXY
      --openstack    Enable if is a pkg for Openstack
```

To work is necesary to apply https://github.com/clearlinux/autospec/pull/331 into your autospec tool

The list of packages for openstack are:

https://github.com/openstack/requirements/blob/master/global-requirements.txt

The etherpath to track the progress:

https://etherpad.openstack.org/p/clr-openstack-pkgs

TODO:

set proper version on the do_openstack_pkg.py script that openstak needs
