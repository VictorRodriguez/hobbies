package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"text/tabwriter"
	"time"
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

func print_help() {
	flag.Usage()
	os.Exit(0)
}

// Name in => /proc/%i/comm
// command line in => /proc/%i/cmdline
// Memory in => /proc/%i/smaps

func monitor(delay int, process_name string) {
	for {
		time.Sleep(time.Duration(delay) * time.Millisecond)
		scan(process_name)
	}
}

func scan(process_name string) {

	w := new(tabwriter.Writer)
	w.Init(os.Stdout, 8, 8, 0, '\t', 0)

	defer w.Flush()

	fmt.Fprintf(w, "\n %s\t%s\t%s\t", "Process Name", "PID", "PSS Memory (Kb)")
	fmt.Fprintf(w, "\n %s\t%s\t%s\t", "------------", "----", "--------------")

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
				if process_name == "" {
					slices_process = append(slices_process, p)
					total_PSS_kb += p.PSS_kb
				} else {
					if process_name == p.name {
						slices_process = append(slices_process, p)
						total_PSS_kb += p.PSS_kb
					}

				}
			}
		}
	}

	sort.SliceStable(slices_process, func(i, j int) bool {
		return slices_process[i].PSS_kb < slices_process[j].PSS_kb
	})

	for _, proc := range slices_process {
		fmt.Fprintf(w, "\n %s\t%d\t%d%s", proc.name,
			proc.pid, proc.PSS_kb, " Kb")
	}

	if (len(slices_process)) > 0 {
		fmt.Fprintf(w, "\n\n %s\t%d\t%s\t\n", "Total", total_PSS_kb, " Kb")
		fmt.Fprintf(w, " %s\t%d\t%s\t\n", "Total", total_PSS_kb/1000, " Mb")
		fmt.Fprintf(w, " %s\t%d\t\n", "Total number of processes: ",
			len(slices_process))
	} else {
		fmt.Println("Process not found")
		print_help()
	}
}

func main() {

	var process_name string
	var delay int

	process_name = ""
	delay = 1000

	monitorPtr := flag.Bool("m", false, "Monitor Mode")
	process_namePtr := flag.String("p", "",
		"Process name to measure PSS memory")
	flag.Parse()

	if *process_namePtr != "" {
		process_name = *process_namePtr
	}

	if *monitorPtr {
		//TODO implement a thread that monitor every X seconds/ms
		monitor(delay, process_name)
		os.Exit(0)
	}

	scan(process_name)
}
