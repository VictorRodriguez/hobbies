import re
dict_cpu = {}
dict_ram = {}
dict_os = {}
list_comb = []

def read_file(filename):
    d = {}
    with open(filename) as f:
        for line in f:
            (key, val) = line.split(",")
            d[key.strip()] = val.strip()
    return d

def create_comb():
    for key_cpu, value_cpu in dict_cpu.items():
        for key_ram, value_ram in dict_ram.items():
            for key_os, value_os in dict_os.items():
                comb = key_cpu + key_ram + key_os
                print(comb)
                list_comb.append(str(comb))
    print("\n")

def apply_rules():
    rules = read_file("rules.txt")
    if rules:
        for key_rule, value_rule in rules.items():
            rule = str(value_rule)
            print("\nRule: "+ rule + "\n")
            p = re.compile(rule)
            for element in list_comb:
                if p.match(element):
                    print(element)

if __name__ == "__main__":
    dict_cpu = read_file("cpu.txt")
    dict_os = read_file("os.txt")
    dict_ram = read_file("ram.txt")
    print("Total Combinations:\n")
    create_comb()
    total_comb = len(dict_cpu)*len(dict_os)*len(dict_ram)
    print("Total number of comb: " + str(total_comb))

    print("\nCombinations with rules")
    apply_rules()

