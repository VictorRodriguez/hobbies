..  This work is licensed under a Creative Commons Attribution 3.0 Unported
    License.
    http://creativecommons.org/licenses/by/3.0/legalcode

================================================
StarlingX: Build system architecture for multiOS
================================================

Storyboard: https://storyboard.openstack.org/#!/story/2004415

Starling X is growing as an edge cloud solution, however, the current cloud use
more than one kind of operating system. A recent analysis of  the most used
operating systems on the Compute Cloud (EC2) [1] shows Ubuntu as the most used
OS, in the same list we can find CentOS and Red Hat Enterprise Linux (RHEL).
Today, Starling X is only based on the CentOS operating system, however, by
having MultiOS support for the STX project the STX developers/users at the
community could benefit from the advantages that each operating system offers.

The current build system under STX does not support the transition to other OS
based on rpm or deb files. In order to give full support for another operating
systems we are proposing to make changes to the current build model and
generate a speration of source code vs build metadata for the STX flock
services. All this with the aim of making it easier for others to understand
and contribute to our project.

Problem description
===================

The diversity on the operating systems used at the cloud is not only for the
guest OS, but also for the host OS. Current cloud systems use a different kind
of operating system as host for their servers. Among the most used OS,
CentOS/RHEL represents approximately 55% of OpenStack and Ubuntu Server
represents 35% of deployments

Since Linux distributions have many different approaches to pulling together
Linux solutions, by having MultiOS support for the STX project the STX
developers/users at the community could benefit from the advantages that each
the operating system offers:

- CentOS uses a more conservative approach and uses older versions of packages and keep security and stability by  backport many fixes and features to their current version.

- Ubuntu is more aggressive and uses more recent versions

- Clear Linux OS is an open source, rolling release Linux distribution optimized for performance and security for the x86 platforms, since a high percentage of the data center servers are based on x86 architectures, enable Starling X in an x86 optimized OS could benefit the STX users

Currently the StarlingX build system only generates RPMs specifically for
CentOS7. The tooling understands how to parse the metadata (srpm_path,
build_srpm) and then patch and re-builds the SRPM, if needed, then the OS and
StarlingX RPM spec-files are parsed and built. There is a dependency generator
that can be used after the first complete build to reduce the build time.
Additionally, there are checks to determine if a package needs to be rebuilt.

The existing build system cannot modify or build other Linux/GNU based
Operating Systems as they use different packaging systems or versions of
packages that are getting patches applied (that may not apply to a different
version).

STX build tools only generate RPMs for CentOS operating system due to two main
reasons:

- RPMs cannot be installed on Ubuntu/Debian

In Ubuntu Linux, installation of software can be done on using Ubuntu Software
Center, Synaptic package manager or apt-get command line mode. Current STX
solution with YUM or rpm install does not work. Ubuntu documentation recommends
to use Alien tool to transfer RPMs to DEB files, however, it can lead to
dependency issues or runtime crashes

- STX RPMs has hardcoded runtime and build requirements for CentOS

CentOS RPMs can have dependencies on package names and versions of software
that may not match what is contained in other distributions such as Ubuntu or
Clear. Additionally RPM spec-files may contain commands (pre/post scripts) that
are not available in other distributions.

The current build system is smart enough to detect missing dependencies and
what packages to rebuild if one package has a change. This feature should
remain on any multi-OS strategy.

STX developers need to have a solid solution for multiple OSes where they want
to deploy STX solution on either RPMs based or DEBs based OSes. The current STX
build system only supports the build of a distro based on CentOS and RPMs, this
specification is written to create a methodology that covers not only the
CentOS RPMs but also a Ubuntu distro based on deb files.

Use Cases
=========

a) End-user can select the Linux OS used for the host OS: If developers need to
generate an image based on alternate OSes for some End User client or Deployer.

b) Developers need to apply a bug fix, feature, or security fix for the
same package on multiple operating systems.

c) Operators that want alternate Operating System other than CentOS in both the
host OS and container guest OS.

d) A developer shall be able to build with unstaged changes for all the
supported OS using the same toolset in their workstation. (this  sounds similar
to "b)" but the difference is to point that as part  of the workflow the devs
needs to test their changes in different  OS and use the same toolset for that
purpose)

e) The build system shall be able to generate installer files for  all
supported OS.

Proposed change
===============

If this change is completed the end to end big picture for the developer/user
will be:

- The user can select the Linux OS used for the host OS

- The user can select the Linux OS used for the containers used in a starling x deployment

- The selection of the host OS and the container OS is independent

- The default operating system to build will be CentOS / RHEL.

- The build system will use the Linux distribution build systems to ensure the distribution is consistent

- The nightly build will use the same mechanisms and the developer build to ensure consistent build output.

- Proper documentation to the developer documentation as STX Developer’s Guide

- Developer workflow with multi-OS will be minimized.

- The definition of how a package is built for a specific Linux distribution will be separated from the actual source code to simplify the addition of other Linux distributions.

In order to achieve these goals, this specification proposes a step-wise
approach with a number of an additional specification that will break down the
steps outlined below:

- Reorganize the STX Flock source, a specification will be created to detail the
implementation. The source and build specific metadata should be separated to
allow for better workflow, this would include creating git repos for each flock
service and their packaging metadata (spec-files, deb rules), adding
appropriate infrastructure tooling to these components, such as autotools.
Autotools provides a mechanism to generate OS specific makefiles, python
setuptools based on templates and ensures the correct build time dependencies
are in place. The "Source Reorg" specification will detail the proposed directory
layout and tools and build targets. Initially, the StarlingX flock could be
built manually and installed based on this new layout.

- Reorganize the StarlingX Integration and packaging repository: specification to
organize the build management code for multiple operating systems. This
specification could explain how the patches and spec files could be reorganized
inside the stx-integ repository.

- The next specification will be the "Dependency Generator" specification, which
would spell out how the dependencies could be generated for multiple packaging
formats or in a package independent fashion.

- The existing build tools would also need to be modified to support the new
directory layout, dependency generation and have different packaging support.
This will also require a specification.

- The installer and configuration management would need to be addressed as well
as the updater process, these would need specification as appropriate and will
be later in the process.

Alternatives
============

A possible alternative is to use Bitbake and create recipes for the Flock,
modified kernel package and modified userspace packages. By using a sub-set of
recipes and the Bitbake fetcher to get the upstream rpm, SRPM, deb or .tar.gz
(as appropriate), one can then build the packages using the native compiler
and tools. Since Bitbake already contains a dependency generator, task
scheduler, and a fetcher it can be used to generate the binary packages. It can
also be used to generate ISOs.

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

Other Deployer impact
=====================

None

Developer impact
=================

Developers would need to understand that the tools and metadata now support
multiple operating systems and the effect that a change they need to make would
mean on those different OSes.

Upgrade impact
===============

None

Implementation
==============

Implementation will be the generation of the following additional
specifications:

Source Reorg
Dependency Generator
Build Tool for MultiOS
ISO Generation for MultiOS
Installer for MultiOS
Configuration management
Update management

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

- Create Specifications listed at Implementation section

Dependencies
============


Testing
=======

Create unit tests for build system

Generate a CI/CD that builds daily an image of each Linux flavor :

- Ubuntu
- CentOS
- Clear Linux

And then run a basic test that proves:

- Boot
- The launch of VMs with Open Stack
- Minimal STX application

Documentation Impact
====================

New documentation will be generated for this multi-OS case

References
==========

[1] https://thecloudmarket.com/stats#/by_platform_definition


History
=======

.. list-table:: Revisions
      :header-rows: 1

   * - Release Name
     - Description
   * - 2019.05
     - Introduced
