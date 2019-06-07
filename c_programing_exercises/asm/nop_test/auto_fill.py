LIMIT = 100000000

def print_many_nops(fout):
    count = 0
    while(count < LIMIT):
        fout.write("nop\n")
        count = count+1


fname = "nop_auto.asm.template"
fout = "nop_auto.asm"

with open(fname) as fin:
    with open(fout, "w") as fout:
        content = fin.readlines()
        for line in content:
            fout.write(line)
            if "nop" in line:
                print_many_nops(fout)
