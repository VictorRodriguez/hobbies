..  This work is licensed under a Creative Commons Attribution 3.0 Unported
    License.
    http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
StarlingX: Reorganize Flock Servie Source code
==============================================

Storyboard: <need Story here>

StarlingX currently combines source code and build meta-data in the same
directory structure, as we move to support multiple OSes, this structure
needs to be seperated and further defined.


Problem description
===================

The current dirtectory structure is based around the build working with CentOS
OS and the current build tooling, as we add additional OS support, additional
meta-data is needed and should be added into a new structure.



Use Cases
=========

a) Devepolers need to support multiple OSes beyond the current CentOS


Proposed change
===============

Reorganize the existing source code to seperate the build meta-data from the
base source code and create indvidial git repos for each STX Flock
sub-component.

One example of a package with multi OS support could be:

::

    <package_name>/
    ├── ubuntu
    │   ├── patches
    │   │   └── cve_fix.patch
    │   ├── rules
    │   └── <package_name>.dsc
    ├── centos
    │   ├── cve_fix.patch
    │   ├── improve_perf.patch
    │   ├── <package_name>.spec
    ├── clear
    │   ├── autospec files
    │   └── cve_fix.patch
    └── fedora
        ├── <package_name>.spec
        └── cve_fix.patch


Alternatives
============

Keep the existing directory structure and add additional sub-directories for 
the new Operating Systems, which will clutter the 

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
of the development, having delimitated the boundaries of each package and how
they are built.

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
   - Victor Rodriguez

Other contributors:
   - Jesus Ornelas
   - Mario Carrillo

Repos Impacted
==============

https://git.starlingx.io/cgit/stx-integ/

Work Items
===========

- Enable Autotools build systems in STX projects: make/make install
- Generate a tar.gz for every STX source code project
- Generate .spec and .rules for each package that STX modify or provide
- Modify the existing build tools to parse the refactored meta-data

Dependencies
============


Testing
=======

- Build and install package for existing CentOS with modified tooling
- Manually build and install packages for alternate operating systems

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
   * - 2019.03
     - Introduced
