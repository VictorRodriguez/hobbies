import os
import csv

list_pkgs_avx2 = []
list_pkgs_avx512 = []

def write_to_csv(avx512_list,avx2_list):
    os.system("rm -rf log.csv")
    for element in avx2_list:
        tmp = []
        if element in avx512_list:
            with open('log.csv', 'a') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                tmp.append(element)
                tmp.append(element)
                wr.writerow(tmp)
        else:
            with open('log.csv', 'a') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                tmp.append(element)
                tmp.append("")
                wr.writerow(tmp)

def find_avx512():
    global list_pkgs_avx512

    with open('log_skylake') as f:
        lines = f.readlines()
        for line in lines:
            element = line.strip()
            if element not in list_pkgs_avx512:
                list_pkgs_avx512.append(element)

def find_avx2():
    global list_pkgs_avx2

    with open('log_haswell') as f:
        lines = f.readlines()
        for line in lines:
            element = line.strip()
            if element not in list_pkgs_avx2:
                list_pkgs_avx2.append(element)

def main():
    if os.path.exists("log") and os.path.exists("log_skylake") and  os.path.exists("log_haswell"):
        pass
    else:
        os.system("grep -R '/haswell/' &> log")
        os.system("find . -name '*.spec*' -exec grep -H 'march=skylake' {} \; | cut -d ':' -f1 | sort -u | cut -d '/' -f2 > log_skylake")
        os.system("find . -name '*.spec*' -exec grep -H 'march=haswell' {} \; | cut -d ':' -f1 | sort -u | cut -d '/' -f2 > log_haswell")

    with open('log') as f:
        lines = f.readlines()
        for line in lines:
            if ".spec" in line:
                if "/haswell"in line and "/avx512" not in line and "#" not in line:
                    pgk = line.split("/")[0]
                    list_pkgs_avx2.append(pgk)

                if "/avx512" in line and "#" not in line:
                    pgk = line.split("/")[0]
                    list_pkgs_avx512.append(pgk)

        find_avx512()
        find_avx2()

        avx2_list=sorted(set(list_pkgs_avx2))
        avx512_list=sorted(set(list_pkgs_avx512))
        
        print("packages with AVX2 : ",len(avx2_list))
        print("packages with AVX-512: ", len(avx512_list))
        print("packages mising AVX-512: ", len(avx2_list) - len(avx512_list))

        write_to_csv(avx512_list,avx2_list)

if __name__ == "__main__":
    main()
