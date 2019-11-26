cachedir = "/home/vrodri3/.launchpadlib/cache/"

import sys
from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously\
    ('lplib.cookbook.json_fetcher', 'production', cachedir, version = 'devel')
project = launchpad.projects['starlingx']

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

bugs_cves = []
bug_dic={}

def get_lps_for_cves():
    tasks = project.searchTasks(status = STATUSES)
    for task in tasks:
        bug = task.bug
        if "CVE" in bug.title or "cve" in bug.title:
            bug_dic['id'] = bug.id
            bug_dic['title'] =  bug.title
            bug_dic['link'] = bug.self_link
            bugs_cves.append(bug_dic)

def cve_assigned(cve_id):
    if not bugs_cves:
        sys.exit(-1)
    for bug in bugs_cves:
        print (bug)
    return False


def main():
    cve_id = "CVE-2018-1002105"
    get_lps_for_cves()
    ret = cve_assigned(cve_id)
    if ret:
        print("%s,%s"%(cve_id,ret))

if __name__== "__main__":
    main()
