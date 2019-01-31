..  This work is licensed under a Creative Commons Attribution 3.0 Unported
    License.
    http://creativecommons.org/licenses/by/3.0/legalcode

=============================================================
StarlingX: Reorganize Flock Services Source Code repositories
=============================================================

Storyboard: https://storyboard.openstack.org/#!/story/2004792


StarlingX currently combines source code and build meta-data in the same
directory structure, as we move to support multiple OSes, this structure needs
to be separated and further refined for the benefit of developers in the
community to keep history and source code separated. Simplifying things to a
set of common features also has the dual benefit of making the code structure
easier to understand and contribute to.


Problem description
===================

The current directory structure is based around the build working with CentOS
and the current build tooling. As we add additional OS support, additional
meta-data is needed and should be reorganized into a new structure. We realized
we needed to standardize the structure of our open source projects in order to
reduce the amount of time we spent figuring out how things work. Simplifying
things to a set of common features also had the dual benefit of making it
easier for others to understand and contribute to our projects. There are some
Directory Structures that could open source use as standard [1] [2], right now
we are not using any of that standard directory structure.

This is an initial reorganization of just the StarlingX Flock source a
subsequent specification the “MultiOS Directory Layout” will further define the
layout within the sub-component directory structure.


Use Cases
=========

a) The build system will parse the stx-flock directory tree and treat like the stx-integ, sources will be fetched from

Proposed change
===============

Reorganize the existing source code to separate the build meta-data from the
base source code, this would leave the existing stx-<flock items> git repos
with source code and a new stx-flock git (1 git) for the packaging meta-data
for all the flock subcomponents.

Example of the new stx-flock directory structure:

::
stx-flock/
├── fault
│   ├── fm-api
│   │   └── centos
│   │       └── fm-api.spec
│   ├── fm-common
│   │   └── centos
│   │       └── fm-common.spec
│   ├── fm-mgr
│   │   └── centos
│   │       └── fm-mgr.spec
│   └── fm-restapi
│       └── centos
│           └── fm-restapi.spec
└── nfv
    ├── guest-agent
    │   └── centos
    │       └── guest-agent.spec
    ├── guest-client
    │   └── centos
    │       └── guest-client.spec
    └── guest-comm
        └── centos
            └── guest-comm.spec



Alternatives
============

Keep the existing directory structure and add additional sub-directories for
the new Operating Systems, which will clutter the current repositories.

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

Improve developer experience to isolate each package increasing the modularity
of the development, having delimited the boundaries of each package and how
they are built.

Upgrade impact
===============

None

Implementation
==============

Is possible to create a separate branch for now and merge until is proved that
does not break the build or the sanity of the system

Assignee(s)
===========

Primary assignee:
    - Victor Rodriguez

Other contributors:

Repos Impacted
==============

- https://git.starlingx.io/cgit/stx-clients
- https://git.starlingx.io/cgit/stx-config
- https://git.starlingx.io/cgit/stx-distcloud
- https://git.starlingx.io/cgit/stx-distcloud-client
- https://git.starlingx.io/cgit/stx-fault
- https://git.starlingx.io/cgit/stx-gui
- https://git.starlingx.io/cgit/stx-ha
- https://git.starlingx.io/cgit/stx-nfv
- https://git.starlingx.io/cgit/stx-update

Work Items
===========
- Create development branch on current repositories
- Create a build management repositories for each service
- Copy necessary build scripts to build management repositories
- Test build management repositories in the package build system

Dependencies
============


Testing
=======

After building a proper image with the reorg of the repositories we can:

- Test build management repositories can generate current RPMs
- Build an STX image
- Run sanity tests for generated image

Documentation Impact
====================

Create a section for developer guide, that guide them how to do a proper
development contribution to the project, a good example of this could be:

https://devguide.python.org/

References
==========

[1] https://www.gun.io/blog/maintaining-an-open-source-project
[2] https://github.com/kriasoft/Folder-Structure-Conventions

History
=======

.. list-table:: Revisions
      :header-rows: 1

   * - Release Name
     - Description
   * - 2019.05
     - Introduced
