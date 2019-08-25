import sys
import os
from os import path

INPUT_FILE="stx_srpms.txt"
CENGN_REPO="http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_build/outputs/SRPMS/std/"


def wget_srpm(srpm):
    url = CENGN_REPO + srpm.strip()
    cmd = "wget %s" % (url)
    ret = os.system(cmd)
    if ret:
        print("Error in wget")
        sys.exit(-1)

F = open(INPUT_FILE,"r")
lines = F.readlines()

for srpm in lines:
    srpm = srpm.strip()
    print(srpm)
    if not path.exists(srpm):
        wget_srpm(srpm)

    cmd = "cp %s /tmp/rpmbuild/" % (srpm)
    ret = os.system(cmd)
    if ret:
        print("Error in cp")
        sys.exit(-1)



