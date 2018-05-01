import requests
from PNP_api import PNP_api
import os
import re

pts_test_repo="https://github.com/phoronix-test-suite/test-profiles.git"
build_url = "https://download.clearlinux.org/current/latest"

def main():
    
    current_build = requests.get(build_url).text.strip()
    print("Current build : %s" % (current_build))

    pnp_api = PNP_api()
    pnp_api.set_current_build(current_build)
    test_list = pnp_api.get_all_tests()

    tmp = "git clone %s --depth=1"%(pts_test_repo)
    if(os.path.isdir("test-profiles")):
        os.system("rm -rf test-profiles")
        os.system(tmp)
    else:
        os.system(tmp)

    dirs_list = []
    test_list = []

    for root, dirs, files in os.walk("test-profiles", topdown=False):
        for name in dirs:
            if "pts/" in os.path.join(root, name) or "system/" in \
                    os.path.join(root, name):
                dirs_list.append(os.path.join(root, name))

    for x in sorted(dirs_list):
        #print(x)
        key_word =x.split("/")[2]
        key_word = (re.sub(r'[^\w]', ' ', key_word))
        key_word = re.sub(" \d+", " ", key_word)
        key_word = key_word.rstrip()
        key_word = key_word.replace(" ","-")
        test_list.append(key_word)

    tmp = sorted(list(set(test_list)))
    test_list = []
    for x in tmp: 
        tmp_2 = []
        count = 0
        for item in sorted(dirs_list):
            if x in item:
                tmp_2.append(item)
        if tmp_2:
            test_list.append(tmp_2[-1])
        else:
            print("list empty")
    tmp = sorted(list(set(test_list)))
    for x in tmp:
        print(x)


if __name__ == "__main__":
    main()
