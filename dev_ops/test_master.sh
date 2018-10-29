#!/bin/sh

CGIT_PATH=/home/vrodri3/cgit-repos
CGIT_LOG=/tmp/cgit-checker.log
echo "" > /tmp/results_fetch.csv
echo `date` > $CGIT_LOG
for f in $CGIT_PATH/*;do
    echo "Updating master of $f" >> $CGIT_LOG
    cd $f
    PKG=$(pwd | cut -d'/' -f5 | cut -d'.' -f1)
    git config remote.origin.fetch 'refs/heads/*:refs/heads/*' &>/dev/null
    git --bare fetch &>/dev/null
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "ERROR: master branch does not merge with CLR master" >> $CGIT_LOG
        status_flag_master=1
    else
        status_flag_master=0
    fi
    cd -
    echo "Check merge of devel/master of $PKG" >> CGIT_LOG
    cd /tmp/git-workspace
    rm -rf $PKG
    git clone $f &>/dev/null
    cd $PKG
    git branch -a | grep 'devel' &> /dev/null
    if [ $? == 0 ]; then
        git merge origin/devel &>/dev/null
        ret=$?
        if [ $ret -ne 0 ]; then
            echo "ERROR:devel doesn't merge with clr master" >> $CGIT_LOG
            status_flag_merge=1
        else
            status_flag_merge=0
        fi
    else
        echo "WARNING: devel branch does not exist: pass" >> $CGIT_LOG
        status_flag_merge=0
    fi
    git reset --merge
    cd $WORK_PATH
    echo debug $status_flag_master $status_flag_merge >> $CGIT_LOG
    if [ $status_flag_master -eq 1 ] || [ $status_flag_merge -eq 1 ]; then
        echo "ERROR: in $PKG" >> $CGIT_LOG
        echo "$PKG,1" >> /tmp/results_fetch.csv
    else
        echo "$PKG,0" >> /tmp/results_fetch.csv
    fi
done
