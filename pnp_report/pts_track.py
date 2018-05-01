import requests
from PNP_api import PNP_api

pts_test_repo="https://github.com/phoronix-test-suite/test-profiles.git"
build_url = "https://download.clearlinux.org/current/latest"

def main():
    
    current_build = requests.get(build_url).text.strip()
    print("Current build : %s" % (current_build))

    pnp_api = PNP_api()
    pnp_api.set_current_build(current_build)
    test_list = pnp_api.get_all_tests()
    print("We have a total of %s tests" % (len(test_list)))

if __name__ == "__main__":
    main()
