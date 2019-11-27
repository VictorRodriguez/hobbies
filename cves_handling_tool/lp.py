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


# These filter the types of bugs open)
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
    data = []
    if path.isfile(file_name):
        data = json.load(open(file_name, "r"))
    return data

def search_upstrem_lps():
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
    for bug in data:
        if cve_id in bug["title"]:
            return bug
    return None

def cve_assigned(cve_id):
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

    cve_id = "CVE-2018-15686"
    bug = cve_assigned(cve_id)
    if bug:
        print(bug)
    else:
        print("%s has no LP assigned" % (cve_id))

if __name__ == "__main__":
    main()
