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

Here is an example of creating a simple Debian package from a simple C source
using the Makefile as its build system.

```
mkdir debhello-0.0

├── Makefile
└── src
    └── hello.c

$ cat src/hello.c
#include <stdio.h>
int
main()
{
        printf("Hello, world!\n");
        return 0;
}

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

tar -czf debhello-0.0.tar.gz debhello-0.0/

cd debhello-0.0/
debmake
vim debian/rules

put this in your debian/rules file override_dh_usrlocal: and this will stop dh_usrlocal from running which i think is actually causing you problems.

dpkg-buildpackage
cd ..
sudo dpkg -i debhello_0.0-1_amd64.deb
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


