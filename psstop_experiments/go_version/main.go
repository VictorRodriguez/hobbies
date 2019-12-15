package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"text/tabwriter"
)

type process struct {
	pid    int
	name   string
	PSS_kb uint64
	valid  int
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

// Name in => /proc/%i/comm
// command line in => /proc/%i/cmdline
// Memory in => /proc/%i/smaps

func main() {
	w := new(tabwriter.Writer)
	w.Init(os.Stdout, 8, 8, 0, '\t', 0)

	defer w.Flush()

	fmt.Fprintf(w, "\n %s\t%s\t%s\t", "Process Name", "PID", "PSS Memory")
	fmt.Fprintf(w, "\n %s\t%s\t%s\t", "------------", "----", "---------")

	directory := "/proc/"

	var total_PSS_kb uint64
	total_PSS_kb = 0
	var slices_process []process

	files, err := ioutil.ReadDir(directory)
	check(err)
	for _, f := range files {
		if f.IsDir() {
			if pid, err := strconv.Atoi(f.Name()); err == nil {
				p := process{pid: pid}
				p.PSS_kb = 0

				dat, err := ioutil.ReadFile(directory + f.Name() + "/comm")
				check(err)
				p.name = strings.TrimSuffix(string(dat), "\n")

				file, err := os.Open(directory + f.Name() + "/smaps")
				check(err)
				defer file.Close()

				scanner := bufio.NewScanner(file)
				for scanner.Scan() {
					if strings.Contains(scanner.Text(), "Pss:") {
						s := strings.Split(scanner.Text(), ":")
						reg, err := regexp.Compile("[^0-9]+")
						check(err)
						pss_s := reg.ReplaceAllString(strings.TrimSpace(s[1]), "")
						pss, err := strconv.ParseUint(pss_s, 10, 64)
						check(err)
						p.PSS_kb += pss
					}
				}
				slices_process = append(slices_process, p)
				total_PSS_kb += p.PSS_kb
			}
		}
	}

	sort.SliceStable(slices_process, func(i, j int) bool {
		return slices_process[i].PSS_kb < slices_process[j].PSS_kb
	})

	for _, proc := range slices_process {
		fmt.Fprintf(w, "\n %s\t%d\t%d\t", proc.name, proc.pid, proc.PSS_kb)
	}

	fmt.Fprintf(w, "\n\n %s\t%d\t%s\t\n", "Total", total_PSS_kb, " Kb")
}
