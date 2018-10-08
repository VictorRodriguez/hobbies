#!/bin/sh

CGIT_PATH=/home/vrodri3/cgit-repos
WORK_PATH=$(pwd)
echo "" > results_fetch.csv
for f in $CGIT_PATH/*;do
    echo "Updating master of $f"
    cd $f
    PKG=$(pwd | cut -d'/' -f5 | cut -d'.' -f1)
    git config remote.origin.fetch 'refs/heads/*:refs/heads/*' &>/dev/null
    git --bare fetch &>/dev/null
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "ERROR: master branch does not merge with CLR master"
        status_flag=1
    else
        status_flag=0
    fi
    cd -
    echo "Check merge of devel/master of $PKG"
    cd /tmp/git-workspace
    rm -rf $PKG
    git clone $f &>/dev/null
    cd $PKG
    git branch -a | grep 'devel' &> /dev/null
    if [ $? == 0 ]; then
        git merge origin/devel &>/dev/null
        ret=$?
        if [ $ret -ne 0 ]; then
            echo "ERROR: devel branch does not merge with CLR master"
            status_flag=1
        else
            status_flag=0
        fi
    else
        echo "WARNING: devel branch does not exist: pass"
        status_flag=0
    fi
    git reset --merge
    cd $WORK_PATH
    echo "$PKG,$status_flag" >> $WORK_PATH/results_fetch.csv
done
