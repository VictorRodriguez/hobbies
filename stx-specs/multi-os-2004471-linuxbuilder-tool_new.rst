..  This work is licensed under a Creative Commons Attribution 3.0 Unported
    License.
    http://creativecommons.org/licenses/by/3.0/legalcode

======================================
StarlingX: Multi OS Linux builder tool
======================================

Storyboard: https://storyboard.openstack.org/#!/story/2004471


StarlingX is based on CentOS operating system, however, it is necessary to
give support of the product in other base OS layers. The current build system
under STX will not support the transition to other OS based on rpm or deb
files. In order to give a full support for other operating systems is necessary
to create a tool that makes Linux images based on deb files and in rpms from
other Linux distributions ( e.g. Fedora )


Problem description
===================

STX image creator only supports CentOS based images, users that want to
generate a different Linux image like Ubuntu or Fedora , will not be able to
generate the ISO image with current tools.

Use Cases
=========

For users that want to install STX solution under Ubuntu base OS or different
RPM base OS like Fedora


Proposed change
===============

Linuxbuilder helps STX developers to create a Linux image based on multiple OS
flavors . This project is intended for anyone that wants to build a Linux image
(IMG/ISO/KVM/Cloud) based on RPMs and DEBs.

We create this project to avoid the process to develop your own tools/scripts
for the creation of your customized distribution, this project provides the
tools to do that with a simple command line (e.g. Make).

POC of the project with README and examples:

https://github.com/VictorRodriguez/linuxbuilder

Alternatives
============

Linaro provides a suite of tools used for creating images (only for DEBS). The
tools create Ubuntu and Android images. The most commonly used tools are
linaro-media-create and linaro-android-media-create.

https://github.com/tobetter/linaro-image-tools

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
stx-Ubuntu.iso
stx-clearlinux.iso


Performance Impact
==================

None

Other deployer impact
=====================

None

Developer impact
=================

Extend functionality of STX developers to Ubuntu base systems and other rpm
base OSs to take advantage of these other OSs

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

   - Jesus Ornelas
   - Victor Rodriguez

Other contributors:

Repos Impacted
==============

https://git.starlingx.io/cgit/stx-integ/

Work Items
===========


Dependencies
============

The RPMs or DEBs need to be pre generated. For teh second face of the tool we
cand add a multiOS package builder like , described in "How to build a package
" section of the readme at:

https://github.com/VictorRodriguez/linuxbuilder#how-to-build-a-package


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


History
=======

.. list-table:: Revisions
   :header-rows: 1

   * - Release Name
     - Description
   * - Stein
     - Introduced
