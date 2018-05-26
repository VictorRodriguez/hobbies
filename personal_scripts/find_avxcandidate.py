import subprocess
import argparse
import re

sse_instructions_xmm = []

sse_instructions_xmm.append("paddb")
sse_instructions_xmm.append("paddd")
sse_instructions_xmm.append("paddsb")
sse_instructions_xmm.append("paddsw")
sse_instructions_xmm.append("paddusb")
sse_instructions_xmm.append("paddusw")
sse_instructions_xmm.append("paddw")
sse_instructions_xmm.append("pmaddwd")
sse_instructions_xmm.append("pmulhw")
sse_instructions_xmm.append("pmullw")
sse_instructions_xmm.append("psubb")
sse_instructions_xmm.append("psubsb")
sse_instructions_xmm.append("psubsw")
sse_instructions_xmm.append("psubusb")
sse_instructions_xmm.append("paddusw")
sse_instructions_xmm.append("paddw")
sse_instructions_xmm.append("pmaddwd")
sse_instructions_xmm.append("pmulhw")
sse_instructions_xmm.append("pmullw")
sse_instructions_xmm.append("psubb")
sse_instructions_xmm.append("psubd")
sse_instructions_xmm.append("psubd")
sse_instructions_xmm.append("psubsb")
sse_instructions_xmm.append("psubsw")
sse_instructions_xmm.append("psubusb")
sse_instructions_xmm.append("psubusw")
sse_instructions_xmm.append("psubw")





def analyse_sse(line):
    if "xmm" in line:
        return line
    for sse_inst in sse_instructions_xmm:
        if sse_inst in line:
            return line

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("filename", help = "The filename to inspect")
    args = parser.parse_args()

    filename = args.filename
    out, err = subprocess.Popen(["objdump","-d", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    alllines = out.decode("latin-1")
    lines =  alllines.split("\n")
    

    sse_cnt = 0
    instructions = 0

    for line in lines:
        ret = 0 
        sse_line = ""

        match = re.search(".*[0-9a-f]+\:\t[0-9a-f\ ]+\t([a-zA-Z0-9]+) \
                (.*)", line)
        instructions += 1
        if args.verbose:
            print(line)
        sse_line=analyse_sse(line)
        if sse_line:
            sse_cnt+=1
            if args.verbose:
                print(sse_line)

    print("Porcentage of SSE/XMM instructions/registers :%d " % \
            (sse_cnt/instructions * 100)  + "%")

if __name__ == '__main__':
    main()

