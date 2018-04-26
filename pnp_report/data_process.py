import urllib.request, json
import requests
from bs4 import BeautifulSoup



class Complex:
    def __init__(self):
        self.data = []


def main():
    current_build = '22010'
    test_list = []
    latest_test_list = []

    build_url="https://download.clearlinux.org/current/latest"
    current_build = requests.get(build_url).text.strip()
    print("Current build : %s" % (current_build))

    with urllib.request.urlopen(alltest_url) as url:
        data = json.loads(url.read().decode())


    with urllib.request.urlopen(latest_running_tests) as url:
        data_latest = json.loads(url.read().decode())

    for item in data: 
        test_name = (item["test_name"])
        if "pts" in test_name:
            test_list.append(test_name)

    for item in data_latest: 
        test_name = (item["test_name"])
        if "pts" in test_name:
            latest_test_list.append(test_name)

    total_tests = len(list(set(test_list)))
    test_latest_rel = len(list(set(latest_test_list)))

    print("We have a total of %s tests" % (total_tests))
    print("In latest release %s we ran %s tests" % (current_build,test_latest_rel))
    print("We have a total of %s tests missing/broken !!" % (total_tests - test_latest_rel))
    print()

    print("First 10 : ")

    for item in list(set(test_list) - set(latest_test_list))[:10]:
        print(item)
    
if __name__ == "__main__":
    main()
