#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2019 Intel Corporation
#

"""
Implement system to detect if CVEs has launchpad assigned
"""
import json
from os import path
from launchpadlib.launchpad import Launchpad


# These filter the open bugs
STATUSES = [
    'New',
    'Incomplete',
    'Confirmed',
    'Triaged',
    'In Progress',
    'Fix Committed',
    'Fix Released',
]

CVES_FILE = 'cves_open.json'

def get_cves_file(file_name):
    """
    Get the cves from prev craeted json file
    """
    data = []
    if path.isfile(file_name):
        data = json.load(open(file_name, "r"))
    return data

def search_upstrem_lps():
    """
    Search for launchpads open with CVE or cve in title
    """
    data = []
    cachedir = "/home/vrodri3/.launchpadlib/cache/"
    launchpad = Launchpad.login_anonymously\
        ('lplib.cookbook.json_fetcher', 'production',\
        cachedir, version='devel')
    project = launchpad.projects['starlingx']
    tasks = project.searchTasks(status=STATUSES)
    for task in tasks:
        bug = task.bug
        if ("CVE" in bug.title or "cve" in bug.title):
            bug_dic = {}
            bug_dic['id'] = bug.id
            bug_dic['title'] = bug.title
            bug_dic['link'] = bug.self_link
            data.append(bug_dic)

    with open(CVES_FILE, 'w') as outfile:
        json.dump(data, outfile)
    return data

def find_cve(cve_id, data):
    """
    Find if CVE exist in list
    """
    for bug in data:
        if cve_id in bug["title"]:
            return bug
    return None

def cve_assigned(cve_id):
    """
    Check if CVE exist in json file, if not search in upstream launchpad
    """
    data = get_cves_file(CVES_FILE)
    bug = find_cve(cve_id, data)
    if bug:
        ret = bug
    else:
        data = search_upstrem_lps()
        bug = find_cve(cve_id, data)
        if bug:
            ret = bug
        else:
            ret = None
    return ret

def main():

    """
    Sanity test
    """
    cve_ids = ["CVE-2019-0160",\
        "CVE-2019-11810",\
        "CVE-2019-11811",\
        "CVE-2018-15686",\
        "CVE-2019-10126"]

    for cve_id in cve_ids:
        bug = cve_assigned(cve_id)
        if bug:
            print("\n")
            print(bug)
        else:
            print("\n%s has no LP assigned\n" % (cve_id))

if __name__ == "__main__":
    main()
