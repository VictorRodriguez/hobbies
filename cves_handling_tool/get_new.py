
def get_cves(FILE):
    array = []
    f = open(FILE, "r")
    lines = f.readlines()
    for line in lines:
        if "CVE" in line and not "CVE-ID" in line:
            array.append(line.strip().split("|")[1])
    return array


FILE = "new.csv"
new_array = get_cves(FILE)

FILE = "old.csv"
old_array = get_cves(FILE)

for item in new_array:
    if item in old_array:
        print("CVE existed %s" % (item))
    else:
        print("New CVE %s" % (item))

