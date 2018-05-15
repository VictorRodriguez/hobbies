import urllib.request, json
import requests
from bs4 import BeautifulSoup

#from urls import *

class PNP_api:
    API_URL = "https://clearlinux-resultsboard.zpn.intel.com/api/" 

    def __init__(self):
        self.current_build = 0

    def set_current_build(self,build):
        self.current_build = build

    def get_all_tests(self):

        test_list = []

        with urllib.request.urlopen(PNP_api.API_URL+"test") as url:
            data = json.loads(url.read().decode())

        for item in data:
            test_name = (item["test_name"])
            if "pts" in test_name:
                test_list.append(test_name)

        self.test_list = list(set(test_list))
        return self.test_list

    def get_latest_run_tests(self):

        latest_test_list = []

        tmp = (latest_run_url + self.current_build + "&groupby=test&orderby=test")

        with urllib.request.urlopen(tmp) as url:
            data_latest = json.loads(url.read().decode())

        for item in data_latest:
            test_name = (item["test_name"])
            if "pts" in test_name:
                latest_test_list.append(test_name)

        test_latest_rel = list(set(latest_test_list))
        return test_latest_rel


def main():
    current_build = '22010'
    test_list = []
    latest_test_list = []

    current_build = requests.get(build_url).text.strip()
    print("Current build : %s" % (current_build))

    pnp_api = PNP_api()

    pnp_api.set_current_build(current_build)

    test_list = pnp_api.get_all_tests()
    latest_test_list = pnp_api.get_latest_run_tests()

    print("We have a total of %s tests" % (len(test_list)))

    print("In latest release %s we ran %s tests" % (current_build,len(latest_test_list)))
    print("We have a total of %s tests missing/broken !!" % (len(test_list) - len(latest_test_list)))

    print()
    print("First 10 : ")

    for item in list(set(test_list) - set(latest_test_list))[:10]:
        print(item)

if __name__ == "__main__":
    main()
