
filename="new.csv"

"""
get_cvss : CVSS, Common Vulnerability Scoring System, is a vulnerability
scoring system designed to provide an open and standardized method for rating
IT vulnerabilities. CVSS helps organizations prioritize and coordinate a joint
response to security vulnerabilities by communicating the base, temporal and
environmental properties of a vulnerability.
"""

def get_cvss(cve_id,filename):
    with open(filename,'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if "CVE" in line and not "CVE-ID" in line:
                if cve_id in (line.strip().split("|")[1]):
                    cvss = (line.strip().split("|")[4])
                    return cvss

def get_cves_id(filename):
    cve_ids = []
    with open(filename,'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if "CVE" in line and not "CVE-ID" in line:
                cve_id = (line.strip().split("|")[1])
                if cve_id not in cve_ids:
                    cve_ids.append(cve_id)
    return cve_ids

"""
Implement policy based on
https://wiki.openstack.org/wiki/StarlingX/Security/CVE_Support_Policy
"""

cve_ids = get_cves_id(filename)

for cve_id in cve_ids:
    cvss = float(get_cvss(cve_id,filename))
    if  cvss > 7.0:
        print(cve_id + ": " + str(cvss))




