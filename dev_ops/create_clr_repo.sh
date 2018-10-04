#!/bin/sh

# use as ./create_clr_repo.sh <url to git repository>

CLR_URL="$1"
PKG=$(echo $CLR_URL | cut -d '/' -f5)
CGIT_PATH=/home/vrodri3/cgit-repos

echo "Cloning $PKG for STX infra"
git clone --bare $CLR_URL $CGIT_PATH/$PKG-stx-clr.git
cp git-hooks/update $CGIT_PATH/$PKG-stx-clr.git/hooks/
echo "Clear Linux $PKG repository" > $CGIT_PATH/$PKG-stx-clr.git/description

