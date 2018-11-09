# How to build deb files

These are personal examples to document how to build debian files for my own
experiance: 

## How to build a package that already exist in debian

Following the next link:
    
    https://wiki.debian.org/BuildingTutorial

These are the steps
 
 * Open your /etc/apt/sources.list file and check if you have one or more lines
   that start with deb-src.

 * sudo apt-get update

 * mkdir -p src/debian/; cd src/debian

 * sudo apt-get install fdupes

 * apt-get source fdupes

 * You have now downloaded the 3 files (.dsc, .tar.gz, .diff.gz), composing the
   Debian source package.

 * Once the package is downloaded, you can check the directory where you are ,
   and you'll find that apart from the 3 files that were downloaded you also
   have a directory, called fdupes-1.50-PR2. This is the unpacked source of the
   Debian package.

 * Every Debian (or Debian derivative) package includes a debian directory,
   where all the information related to the Debian package is stored. Anything
   that's outside of that directory, is the upstream code, i.e. the original
   code released by whoever programmed the software.

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

    debuild -b -uc -us

 * Install this file with:
    
    sudo dpkg -i ../fdupes_1.50-PR2-3_<your arch>.deb










## How to build a package from tar.gz


