from lxml import html
import requests
import sys
import os


def get_score(tree):
    res = tree.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()')
    if  (len(res) > 0):
        score = res[0].strip()
    else:
        score = "Not found"
    return score

def get_attack_vector(tree):
    res = tree.xpath('//span[@data-testid="vuln-cvssv3-av"]/text()')
    if  (len(res) > 0 ):
        av = res[0].strip()
    else:
        av = "Not found"
    return av


CVEs = []
final_list = []

if  len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as cve_file:
            CVEs = cve_file.readlines()
        for element in CVEs:
            final_list.append(element.strip())
        CVEs = final_list
    else:
        cve_id = str(sys.argv[1])
        if "CVE" in cve_id:
            CVEs.append(cve_id)

print("CVE-id,score,Attack Vector")
for cve in CVEs:
    page = "https://nvd.nist.gov/vuln/detail/" + cve
    page = requests.get(page)
    tree = html.fromstring(page.content)
    score = get_score(tree)
    av = get_attack_vector(tree)
    print("%s,%s,%s" % (str(cve),str(score),str(av)))

