import requests
from PNP_api import PNP_api
import os
import re
from distutils.version import LooseVersion

pts_test_repo="https://github.com/phoronix-test-suite/test-profiles.git"
build_url = "https://download.clearlinux.org/current/latest"

def main():

    current_build = requests.get(build_url).text.strip()
    print("Current build : %s" % (current_build))

    pnp_api = PNP_api()
    pnp_api.set_current_build(current_build)
    pnp_tests = pnp_api.get_all_tests()

    if(os.path.isdir("test-profiles")):
        os.system("rm -rf test-profiles")
    os.system("git clone %s --depth=1"%(pts_test_repo))

    phoronix_tests = []
    for prefix in ["pts", "system"]:
        for test in os.listdir(os.path.join("test-profiles", prefix)):
            version = test.split("-")[-1]
            name = test[:-(len(version)+1)]
            phoronix_tests.append(os.path.join(prefix, name))

    missing = set(phoronix_tests) - set(pnp_tests)
    print("Missing tests:")
    for x in sorted(list(missing)):
        print(x)


if __name__ == "__main__":
    main()
