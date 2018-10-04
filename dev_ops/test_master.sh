#!/bin/sh


CGIT_PATH=/home/vrodri3/cgit-repos
WORK_PATH=$(pwd)
echo "" > results_fetch.csv
for f in $CGIT_PATH/*;do
    echo "Updating master of $f"
    cd $f
    PKG=$(pwd | cut -d'/' -f5 | cut -d'.' -f1)
    echo $PKG
    git config remote.origin.fetch 'refs/heads/*:refs/heads/*'
    git --bare fetch
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "ERROR: master branch does not merge with CLR master"
        echo "$PKG,1" >> $WORK_PATH/results_fetch.csv
    fi
done

