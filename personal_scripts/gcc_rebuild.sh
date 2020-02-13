#!/bin/bash


# minimal packages to build a linux system , taken from :
# http://www.linuxfromscratch.org/lfs/view/6.6/index.html
# systemd is exrta, but is evil when gcc change :)

declare -a arr=("binutils"\
    "gcc" \
    "linux" \
    "glibc"\
    "tcl"\
    "expect"\
    "dejagnu"\
    "ncurses"\
    "bash"\
    "bzip2"\
    "coreutils"\
    "diffutils"\
    "gawk"\
    "gettext"\
    "grep"\
    "gzip"\
    "m4"\
    "make"\
    "patch"\
    "perl"\
    "sed"\
    "tar"\
    "texinfo"\
    "autoconf"\
    "automake" \
    "bison"\
    "e2fsprogs"\
    "expect"\
    "file"\
    "findutils" \
    "flex" \
    "gdb" \
    "groff" \
    "ncurses" \
    "patch" \
    "perl" \
    "pkg-config" \
    "tcl" \
    "nss" \
    "systemd" \
    )

function build_lfs() {
for package in "${arr[@]}"
do
    build $package
done
}

function build_all() {
for package in `find packages/ -type d -maxdepth 1`
do
    make clone_$package
    build $package
done
}


function build(){
    if [ -d "packages/$1" ]; then
        echo
        echo "  Building packages/$1"
        echo
        pushd packages/$1
            make &> build_out.log
            if [ $? -eq 1 ]
            then
                echo
                echo "ERROR: $1 not building, time to debug"
                echo
                echo $1 >> ~/failing_pkgs.log
            else
                echo
                echo "Copy RPMS to repo"
                echo
                cp results/*.rpm /home/repo
                createrepo_c /home/repo
            fi
        popd
    else
        echo
        echo "$1 dir does not exist"
        echo
    fi
}

build_lfs

