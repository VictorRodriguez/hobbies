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
    ./do_openstack_pkg.py <PKG-NAME> openstack
```

The list of packages for openstack are:

https://github.com/openstack/requirements/blob/master/global-requirements.txt

The etherpath to track the progress:

https://etherpad.openstack.org/p/clr-openstack-pkgs

TODO:

set proper version on the do_openstack_pkg.py script that openstak needs
