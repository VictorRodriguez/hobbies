from lxml import html
import requests
import sys


cve_d = {}
final_list = []

if  len(sys.argv) > 1:
    with open(sys.argv[1]) as cve_file:
        CVEs = cve_file.readlines()
    for element in CVEs:
        final_list.append(element.strip())
    CVEs = final_list
else:
    CVEs=["CVE-2018-17972"]

for cve in CVEs:
    page = "https://nvd.nist.gov/vuln/detail/" + cve
    page = requests.get(page)
    tree = html.fromstring(page.content)
    scores = tree.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()')
    if  (len(scores) > 0 ):
        cve_d[cve] = scores[0]
    else:
        cve_d[cve] = "Not found"

print cve_d
for key in cve_d.keys():
        print("%s,%s\n"%(key,cve_d[key]))

