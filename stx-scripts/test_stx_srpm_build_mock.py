import sys
import os
import glob
import shutil

TMP="/tmp/rpmbuild"
INPUT_FILE="stx_srpms.txt"
CENGN_REPO="http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_build/outputs/SRPMS/std/"
DEST_DIR=os.path.join(os.getcwd(),"rpms")

def wget_srpm(srpm):
    url = CENGN_REPO + srpm.strip()
    cmd = "wget -P %s %s" % (TMP,url)
    ret = os.system(cmd)
    if ret:
        print("Error in wget")
        sys.exit(-1)


os.system("echo > errors.log")
if not os.path.exists(DEST_DIR):
    os.mkdir(DEST_DIR)

F = open(INPUT_FILE,"r")
lines = F.readlines()

for srpm in lines:
    srpm = srpm.strip()
    print(srpm)
    if not os.path.exists(os.path.join(TMP,srpm)):
        wget_srpm(srpm)

    cmd = "make srpm SRPM=%s MOCK_CONFIG=local-centos-7-x86_64" % (srpm)
    ret = os.system(cmd)
    if ret:
        print("Error in build w/ mock. RET = %d" % (ret))
        os.system("echo %s >> errors.log" % (srpm))

    output = os.path.join(TMP,"output/local-centos-7-x86_64")
    files = glob.iglob(os.path.join(output, "*.rpm"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, DEST_DIR)
