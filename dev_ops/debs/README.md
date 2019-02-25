# How to build deb files

These are personal examples to document how to build Debian files for my own
experience: 

## How to build a package that already exists in Debian

This tutorial, is based on [1], to begin these are the steps:
 
 * Open your /etc/apt/sources.list file and check if you have one or more lines
   that start with deb-src.

 * sudo apt-get update

 * mkdir -p src/debian/; cd src/debian

 * sudo apt-get install fdupes

 * apt-get source fdupes

 * You have now downloaded the 3 files (.dsc, .tar.gz, .diff.gz), composing the
   Debian source package.

 * Once the package is downloaded, you can check the directory where you are, and you'll find that apart from the 3 files that were downloaded you also have a directory, called fdupes-1.50-PR2. This is the unpacked source of the
   Debian package.

 * Every Debian (or Debian derivative) package includes a debian directory,
   where all the information related to the Debian package is stored. Anything that's outside of that directory, is the upstream code, i.e. the original code released by whoever programmed the software.

 * This is the directory that the package maintainer has added to the source
   code to build the package.

 * In this directory you'll usually find lots of files related to Debian's
   version of the program, Debian specific patches, manpages, documentation,
   and so on

    * the rules file is the executable file that we will be running in order to
      build the package.

    * in the patches directory, there are also a number of patches applied by
      the maintainer

 * Get the build dependencies with: sudo apt-get build-dep fdupes

 * Rebuild without changes with
```
    debuild -b -uc -us
```
 * Install this file with:
```
    sudo dpkg -i ../fdupes_1.50-PR2-3_<your arch>.deb
```

At this point, you might be wondering what is the difference between: 

* debuild - build a Debian package
https://manpages.debian.org/jessie/devscripts/debuild.1.en.html

* dpkg-buildpackage - build binary or source packages from sources
https://manpages.debian.org/jessie/dpkg-dev/dpkg-buildpackage.1.en.html


The debuild command is a wrapper script of the dpkg-buildpackage command to
build the Debian binary package under the proper environment variables.

## How to build a package from tar.gz ( simple example ) 

### Big picture

The big picture for building a single non-native Debian package from the upstream tarball debhello-0.0.tar.gz can be summarized as:

* The maintainer obtains the upstream tarball debhello-0.0.tar.gz and untars its contents to the debhello-0.0 directory.
* The debmake command debianizes the upstream source tree by adding template files only in the debian directory.
	* The debhello_0.0.orig.tar.gz symlink is created pointing to the debhello-0.0.tar.gz file.
	* The maintainer customizes template files.
* The debuild command builds the binary package from the debianized source tree.
	* debhello-0.0-1.debian.tar.xz is created containing the debian directory.

```
 $ tar -xzmf debhello-0.0.tar.gz
 $ cd debhello-0.0
 $ debmake
   ... manual customization
 $ debuild
   ...
 ```

The debmake command is the helper script for the Debian packaging.

* It always sets most of the obvious option states and values to reasonable defaults.
* It generates the upstream tarball and its required symlink if they are missing.
* It doesn’t overwrite the existing configuration files in the debian/ directory.
* It supports the multiarch package.
* It creates good template files such as the debian/copyright file compliant with DEP-5.

After debmake debuild command build the package

### Commands to build:

Here is a summary of commands similar to the debuild command.

* The debian/rules file defines how the Debian binary package is built.
* The dpkg-buildpackage command is the official command to build the Debian binary package. For normal binary build, it executes roughly:
	* “dpkg-source --before-build” (apply Debian patches, unless they are already applied)
	* “fakeroot debian/rules clean”
	* “dpkg-source --build” (build the Debian source package)
	* “fakeroot debian/rules build”
	* “fakeroot debian/rules binary”
	* “dpkg-genbuildinfo” (generate a *.buildinfo file)
	* “dpkg-genchanges” (generate a *.changes file)
	* “fakeroot debian/rules clean”
	* “dpkg-source --after-build” (unapply Debian patches, if they are applied during --before-build)
	* “debsign” (sign the *.dsc and *.changes files)

* The debuild command is a wrapper script of the dpkg-buildpackage command to build the Debian binary package under the proper environment variables.
* The pdebuild command is a wrapper script to build the Debian binary package under the proper chroot environment with the proper environment variables.
* The git-pbuilder command is another wrapper script to build the Debian binary package under the proper chroot environment with the proper environment variables. This provides an easier command line UI to switch among different build environments.

## Example

Here is an example of creating a simple Debian package from a simple C source
using the Makefile as its build system.

Structure of directory:

```
mkdir debhello-0.0

├── Makefile
└── src
    └── hello.c
```

Source code:

```
$ cat src/hello.c
#include <stdio.h>
int
main()
{
        printf("Hello, world!\n");
        return 0;
}
```
Makefile:

```
$ cat Makefile
prefix = /usr/local

all: src/hello

src/hello: src/hello.c
	@echo "CFLAGS=$(CFLAGS)" | \
		fold -s -w 70 | \
		sed -e 's/^/# /'
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDCFLAGS) -o $@ $^

install: src/hello
	install -D src/hello \
		$(DESTDIR)$(prefix)/bin/hello

clean:
	-rm -f src/hello

distclean: clean

uninstall:
	-rm -f $(DESTDIR)$(prefix)/bin/hello

.PHONY: all install clean distclean uninstall
```
Create tarball: 
```
tar -czf debhello-0.0.tar.gz debhello-0.0/
```

After that is possible to start with packaging:

```
cd debhello-0.0/
debmake

```

Adjsut the override_dh_usrlocal:
```
vim debian/rules
#!/usr/bin/make -f
# You must remove unused comment lines for the released package.
export DH_VERBOSE = 1
#export DEB_BUILD_MAINT_OPTIONS = hardening=+all
export DEB_CFLAGS_MAINT_APPEND  = -Wall -pedantic
export DEB_LDFLAGS_MAINT_APPEND = -Wl,--as-needed

%:
	dh $@

override_dh_usrlocal:

#override_dh_auto_install:
#	dh_auto_install -- LIBDIR=/usr/local/lib

#override_dh_install:
#	dh_install --list-missing -X.pyc -X.pyo
```
Build 
dpkg-buildpackage -B

Check that all binaries are installed in DEB
```
cd ..
sudo dpkg -c debhello_0.0-1_amd64.deb
hello
```

In the end the only file that is necesary is the DSC file
DSC = Debian source packages' control file format
Details of each filed on the DSC file at [ubuntu-manpages](http://manpages.ubuntu.com/manpages/bionic/man5/dsc.5.html)


If you have the DSC file you just need to: 

```
dpkg-source -x foo_version.dsc
```
change into the extracted source directory. Then run:

```
dpkg-buildpackage -rfakeroot -b
```


More info at : 
https://www.debian.org/doc/manuals/debmake-doc/ch04.en.html


## How to build a package from tar.gz ( more complex example ) 

More instructions at: 

https://www.debian.org/doc/manuals/debmake-doc/ch08.en.html

## Where does the debian repositories live: 

Examples: 

 * GLIBC:   https://salsa.debian.org/glibc-team/glibc/tree/sid
 * GCC:     https://salsa.debian.org/toolchain-team/gcc-cross 

### Links

    https://wiki.debian.org/BuildingTutorial


