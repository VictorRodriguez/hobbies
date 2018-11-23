..  This work is licensed under a Creative Commons Attribution 3.0 Unported
    License.
    http://creativecommons.org/licenses/by/3.0/legalcode

=======================
StarlingX: Multi OS build architecture
=======================

Storyboard: https://storyboard.openstack.org/#!/story/2004415

Starling X is based on CentOS operating system, however, is necessary to give
support of the product in other base OS layers. The current build system under
STX will not support the transition to other OS based on rpm or deb files. In
order to give a full support for other operating systems is necessary to
refactor the current build model and generate an isolation of source code of stx
flock services, patches, and build tools


Problem description
===================

STX build tools generate only RPMs for CentOS operating system due to two main
reasons:

- STX RPMs cannot be installed on Ubuntu/Debian

In Ubuntu Linux, installation of software can be done on using  Ubuntu Software
Center or  Synaptic package manager or apt-get command line mode.  Current STX
solution with YUM or rpm install does not work. Ubuntu documentation recommends
to use Alien ( described in Alternatives section) tool to transfer RPMs to DEB
files, however, it can lead to dependency issues or runtime crashes
  
- STX RPMs has hardcoded runtime and build requirements for CentOS

CentOS RPM's can have dependencies on versions of software that do not exist on
Fedora and vice versa. For example , CentOS kernel spec file has the following
Build requirements: 


::
 
    BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
    BuildRequires: xz, findutils, gzip, m4, perl, make >= 3.78, diffutils, gawk
    BuildRequires: gcc >= 4.8.5-29, binutils >= 2.25, redhat-rpm-config >= 9.1.0-55
    BuildRequires: hostname, net-tools, bc
    BuildRequires: xmlto, asciidoc
    BuildRequires: openssl
    BuildRequires: hmaccalc
    BuildRequires: python-devel, newt-devel, perl(ExtUtils::Embed)
    BuildRequires: pesign >= 0.109-4
    BuildRequires: elfutils-libelf-devel
    BuildRequires: sparse >= 0.4.1
    BuildRequires: elfutils-devel zlib-devel binutils-devel bison
    BuildRequires: audit-libs-devel
    BuildRequires: java-devel
    BuildRequires: numactl-devel
    BuildRequires: pciutils-devel gettext ncurses-devel
    BuildRequires: python-docutils
    BuildRequires: zlib-devel binutils-devel
    BuildRequires: rpm-build >= 4.9.0-1, elfutils >= 0.153-1
    BuildRequires: bison flex
    BuildRequires: glibc-static

Many of these do not exist with that specific name on RPMs base distributions such as
Fedora: 

https://src.fedoraproject.org/rpms/kernel/blob/master/f/kernel.spec

Or Clear Linux: 

https://github.com/clearlinux-pkgs/linux/blob/master/linux.spec

Apart from this, it is also very possible that Fedora RPM's will use macros in
RPM pre- and postscripts that are unavailable on CentOS or try to do stuff in
those scripts that are not possible on CentOS.

That said, it is not impossible to use Fedora RPM's on CentOS. but will not
work 100% of the times. What is probably safer, is to rebuild and refactor each
SRPM on the new target OS. This will make the build requirement and runtime
requirement warnings/ errors came up during the rebuild and are fixed before
deploying the software to customers


The current build system is very smart to detect missing dependencies and
what packages to rebuild if one package has a change. However, making the same
logic of other 3 OSs will not scale. 

STX developers need to have a solid solution for multiple OSs where they want
to deploy STX solution either RPMs base or DEBs base OSs


Use Cases
=========

Use cases: 

a) Developers need to generate an image based on Ubuntu for some End User
client or Deployer

b) If developers need to apply a security fix for the same package on multiple
operating systems customers


Proposed change
===============

- Enable Autotools to build systems in STX projects: make/make install
- Generate a tar.gz for every STX proprietary source code project
- Generate .spec and .rules for each package that STX modify or provide
- Provide a tool that creates build system environment for developers to build each package for multiple operating systems
- Provide a tool that make .iso image for each flavor or Linux based OS taking upstream repositories, local mirror or local changes
- Provide a tool that generates .img file to boot and test patches to the source code, configuration changes or new features on STX systems


Alternatives
============

- From Current RPMs to DEBs:

There are some alternatives to transform current RPMs to DEBs, the most used
is Alien.

Alien is a program that converts between the rpm, dpkg file formats. If you 
want to use a package from another
distribution than the one you have installed on your system, you can use alien
to convert it to your preferred package format and install it.

A .rpm package can be converted to .deb package using following command: 

sudo alien -to-deb -scripts someone-0.11-4.i386.rpm 

it will generate a .deb package someone_0.11-5_i386.deb

What alien cannot resolve is converting rpm dependencies (both run and build)
to Debian dependencies.

So, here is a solution.. (there might be others).. putting the dependencies
manually.

- convert the rpm package to debian package format directory. use command sudo
   alien –generate –scripts ecedemo-0.11-1.noarch.rpm this will create
   directory someone-0.11/ with deb package like structure.

- now, all you have to do is change the someone-0.11/debian/control file. add
   whatever dependencies you like in the for “Depends: ” tag.
   Depends:sun-java5-jre, slapd

- rebuild deb package from intermediate directory cd someone-0.11/ sudo
   dpkg-buildpackage

Keep in mind that it typically isn’t a good idea to install packages that were
not meant for your system. It can lead to dependency issues and can cause
errors or even crash. If the software you are installing has some dependencies
that need to be installed, you will need to install these first.

All of these converted packages only increase the chance of the software not
functioning properly, so do this at your own risk. If there is no available
.deb substitute, then compiling the source code on your machine might be a
better choice when possible.  

Another solution is to refactor most of the tools and build scripts from : 

https://git.starlingx.io/cgit

To work with deb build process, described in : 

https://github.com/VictorRodriguez/hobbies/tree/master/dev_ops/debs


- From Current RPMs to other RPMs based distro:


If we do this for every OS requirement (let's take for example that in the
future we need to make this for Fedora or other OS) it will take time and
replication of could be created


Data model impact
=================

None


REST API impact
===============

None

Security impact
===============

None

Other end user impact
=====================

None

In the end, the End user will have: 

stx-centos.iso
stx-ubuntu.iso
stx-clearlinux.iso


Performance Impact
==================

None
 
Other deployer impact
=====================

None

Developer impact
=================

Improve developer experience to isolate each package increasing the modularity
of the development, having delimitated the boundaries of each package and what
patches and CFLAGS are applied to each project

Upgrade impact
===============

None

Implementation
==============

Implementation will be in parallel to the current build system and will be
available for the community to be evaluated and used if needed

Assignee(s)
===========


Primary assignee:
   Victor Rodriguez

Other contributors:
   Jesus Ornelas
   Mario Carrillo

Repos Impacted
==============

https://git.starlingx.io/cgit/stx-integ/

Work Items
===========

- Enable Autotools build systems in STX projects: make/make install
- Generate a tar.gz for every STX proprietary source code project
- Generate .spec and .rules for each package that STX modify or provide
- Provide a tool that creates build system environment for developers to build each package for multiple operating systems
- Provide a tool that make .iso image for each flavor or Linux base OS taking upstream repos, local mirror or local changes
- Provide a tool that generates .img file to boot and test patches to the source code, configuration changes or new features on STX systems


Dependencies
============


Testing
=======

Generate a CI/CD  that builds daily an image of each Linux flavor : 

- Ubuntu
- Centos
- Clear Linux

And then run a basic test that proves: 

- Boot
- Lauch of VMs with Open Stack
- Minimal STX application

Documentation Impact
====================

New documentation will be generated for this multi-OS case

References
==========

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to notes from a summit session

* Links to relevant research, if appropriate

* Related specifications as appropriate (e.g. if it's an EC2 thing, link the
  EC2 docs)

* Anything else you feel it is worthwhile to refer to


History
=======


.. list-table:: Revisions
   :header-rows: 1

   * - Release Name
     - Description
   * - Stein
     - Introduced
