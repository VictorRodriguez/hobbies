..
  This work is licensed under a Creative Commons Attribution 3.0 Unported
  License. http://creativecommons.org/licenses/by/3.0/legalcode

..

=======================
StarlingX: Multi OS build architecture
=======================

Storyboard: https://storyboard.openstack.org/#!/story/2004415


Starling X is based on CentOS operating system, however is necesary to give
support of the product in other base OS layers. The current build system under
STX will not support the transition to other OS based on rpms or deb files. In
order to give a full support for other operating systems is necesary to
refactor current build model and generate an isolation of source code of stx
flock services, patches and build tools


Problem description
===================

STX build tools generate only rpms for CentOS operating system. This will not
be scalable for ussers trying to deploy STX solution on other operating systems
based on debs and rpms. Build system needs to generate debs and rpms for
operating systems such as ubuntu / fedora / clear linux and current centos
using the same build tools

Use Cases
=========

Use cases: 

a) Developers need to generate an image based on Ubuntu for some End User
client or Deploer

b) If developers need to apply a security fix for the same package on multiple
operating systems costumerts


Proposed change
===============

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

At this point, if you would like to just get feedback on if the problem and
proposed change fit in StarlingX, you can stop here and post this for review to
get preliminary feedback. If so please say: Posting to get preliminary feedback
on the scope of this spec.

 Alternatives
============

Refactor most of the tools from : 

https://git.starlingx.io/cgit

If we do this for every OS requirement it will take time and replication of
coudl coudl be created


Data model impact
=================

None


REST API impact
===============

None

Security impact
===============


Other end user impact
=====================

None in the end the usser will have: 

stx-centos.iso
stx-ubuntu.iso
stx-clearlinux.iso


Performance Impact
==================


Other deployer impact
=====================


Developer impact
=================

Discuss things that will affect other developers working on StarlingX.

Upgrade impact
===============

Implementation
==============

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

   0) Enable autotools build systems in STX projects: make / make install
   1) Generate an tar.gz for every STX propietary source code project
   2) Generate .spec and .rules for each package that STX modify or provide
   3) Provide tool that create build system enviroment for developers to build
   each package for multiple operating systems
   4) Provide tool that make .iso image for each flavor or Linux base OS taking
   upstream repos, local mirror or local changes
   5) Provide tool that generate .img file to boot and test patches to source
   code , configuration changes or new features on STX systems


Dependencies
============


Testing
=======



Documentation Impact
====================

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
