
..  This work is licensed under a Creative Commons Attribution 3.0 Unported
    License.
    http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
StarlingX: Define directory layout for MultiOS
==============================================

Storyboard: https://storyboard.openstack.org/#!/story/2004891

This specification will define the current directory layout used by the
current StarlingX build system to allow for future build system(s). There are
currently other directories that contain patches or configuration files, these
files are typically version specific and will need to be considered in any
solution.


Problem description
===================

The current dirtectory structure is based around the build working with CentOS
OS and the current build tooling, as we add additional OS support, additional
meta-data will be needed and should be added into a new structure.

Use Cases
=========

a) Devepolers need to support multiple OSes beyond the current CentOS


Proposed change
===============

Define an extended directory layout that will support other Operating Systems
beyond the existing CentOS layout. The existing layout will remain in place as
the new build system is developed in order to not distrub the current
workflow.


The following is the proposed layout:

::

<package-name>
├── centos-patched
│   ├── build_srpm.data
│   ├── files
│   │   ├── 0001-First-centos-source.patch
│   │   └── centos.conf
│   ├── meta_patches
│   │   ├── 0001-First-centos-spec-file.patch
│   │   └── PATCH_ORDER
│   └── srpm_path
├── centos-unpatched
│   ├── build_srpm.data
│   ├── files
│   │   ├── 0001-First-centos-source.patch
│   │   └── centos.conf
│   └── package.spec
├── clear
│   ├── auto-spec-files
│   └── stx-specific.patch
└── ubuntu
    ├── package.dsc
    └── rules


Alternatives
============

Create a new set of repos to represent each new operating system.

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


Performance Impact
==================

None

Other deployer impact
=====================

None

Developer impact
=================

Developers will need to ensure any changes are correctly rebased and tested
against each upstream Operating system being supported by the current build.

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
   - Erich


Repos Impacted
==============

https://git.starlingx.io/cgit/stx-integ/
https://git.starlingx.io/cgit/stx-upstream/
All Flock related repos currently containing cento meta-data or the new
https://git.starlingx.io/cgit/stx-flock/ if created.

Work Items
===========

- Create directory tree and files as new Operating Systems are added.

Dependencies
============


Testing
=======

Ensure that the current build continues to work as the directory layout is
extended.

Documentation Impact
====================

New documentation will be generated to define the contents of the extended
directory layout.

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
