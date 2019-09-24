"""
Implement policy based on
https://wiki.openstack.org/wiki/StarlingX/Security/CVE_Support_Policy
"""

def get_cvss(cve_id,filename):
    """
    Get the CVSS score of a CVE
    CVSS, Common Vulnerability Scoring System, is a vulnerability
    scoring system designed to provide an open and standardized method for
    rating IT vulnerabilities.
    :param filename: The name of the file with the CVEs metadata
    :param cve_id: ID of the CVE is necesary to get the CVSS score
    :return: return the CVSS score
    """
    with open(filename,'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if "CVE" in line and not "CVE-ID" in line:
                if cve_id in (line.strip().split("|")[1]):
                    cvss = (line.strip().split("|")[4])
                    return cvss

def get_cves_id(filename):
    """
    Get the CVEs ids from the vulscan document
    :param filename: The name of the file with the CVEs metadata
    :return: return the CVE ids as array
    """
    cve_ids = []
    with open(filename,'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if "CVE" in line and not "CVE-ID" in line:
                cve_id = (line.strip().split("|")[1])
                if cve_id not in cve_ids:
                    cve_ids.append(cve_id.strip())
    return cve_ids

def get_base_vector(cve_id,filename):
    """
    Get Base Metrics vector:
    Attack-vector: Context by which vulnerability exploitation is possible.
    Attack-complexity: Conditions that must exist in order to exploit
    Authentication: Num of times that attacker must authenticate to exploit
    Availability-impact: Impact on the availability of the target system.
    return: Attack-vector/ Access-complexity/Authentication/Availability-impact
    """
    with open(filename,'r') as fh:
        vector = None
        av = None
        ac = None
        au = None
        ai = None
        lines = fh.readlines()
        count = 0
        for line in lines:
            count = count + 1
            if cve_id in line and ("UNFIXED" in line\
            or "FIXED" in line):
                tmp_line = lines[count+4].strip()
                if "nvd" in tmp_line:
                    vector = tmp_line.split("|")[2].strip()
                break
        if vector:
            for element in vector.split("/"):
                if "AV:" in element:
                    av = element.split(":")[1]
                if "AC:" in element:
                    ac = element.split(":")[1]
                if "Au:" in element:
                    au = element.split(":")[1]
                if "I:" in element:
                    ai = element.split(":")[1]
        return av,ac,au,ai

if __name__ == '__main__':

    cves_valid = []

    filename="new.csv"
    data_file="full.txt"

    cve_ids = get_cves_id(filename)

    for cve_id in cve_ids:
        cve = {}

        cvss = float(get_cvss(cve_id,filename))
        av,ac,au,ai = get_base_vector(cve_id,data_file)

        """
        Following rules from:
        https://wiki.openstack.org/wiki/StarlingX/Security/CVE_Support_Policy
        """
        if  cvss >= 7.0\
        and av == "N"\
        and ac == "L"\
        and (au == "N" or au == "S")\
        and (ai == "P" or ai == "C"):
            cve["id"] = cve_id
            cve["cvss"] = cvss
            cve["av"] = av
            cve["ac"] = ac
            cve["au"] = au
            cve["ai"] = ai
            cves_valid.append(cve)

    print(cves_valid)

