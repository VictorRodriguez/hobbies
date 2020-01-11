package main

import (
	"bufio"
	"encoding/csv"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
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

func checkError(message string, err error) {
	if err != nil {
		log.Fatal(message, err)
	}
}

func print_help() {
	flag.Usage()
	os.Exit(0)
}

// Name in => /proc/%i/comm
// command line in => /proc/%i/cmdline
// Memory in => /proc/%i/smaps

func write_csv(process_list []process, file_name string) {

	var data = [][]string{}

	for _, proc := range process_list {
		tmp := []string{proc.name, strconv.Itoa(proc.pid),
			strconv.FormatUint(proc.PSS_kb, 10)}
		data = append(data, tmp)
	}

	file, err := os.Create(file_name)
	checkError("Cannot create file", err)
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, value := range data {
		err := writer.Write(value)
		checkError("Cannot write to file", err)
	}
}

func monitor(delay int, process_name string) {
}

func scan(process_name string) ([]process, uint64) {

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

	return slices_process, total_PSS_kb
}

func print_list(process_list []process, total_PSS_kb uint64) {

	w := new(tabwriter.Writer)
	w.Init(os.Stdout, 8, 8, 0, '\t', 0)

	defer w.Flush()

	fmt.Fprintf(w, "\n %s\t%s\t%s\t", "Process Name", "PID", "PSS Memory (Kb)")
	fmt.Fprintf(w, "\n %s\t%s\t%s\t", "------------", "----", "--------------")

	for _, proc := range process_list {
		fmt.Fprintf(w, "\n %s\t%d\t%d%s", proc.name,
			proc.pid, proc.PSS_kb, " Kb")
	}

	if (len(process_list)) > 0 {
		fmt.Fprintf(w, "\n\n %s\t%d\t%s\t\n", "Total", total_PSS_kb, " Kb")
		fmt.Fprintf(w, " %s\t%d\t%s\t\n", "Total", total_PSS_kb/1000, " Mb")
		fmt.Fprintf(w, " %s\t%d\t\n", "Total number of processes: ",
			len(process_list))
	} else {
		fmt.Println("Process not found")
		print_help()
	}
}

func main() {

	var process_name string
	var csv_file_name string
	var delay int
	var process_list []process

	process_name = ""
	csv_file_name = ""
	delay = 1000

	var total_PSS_kb uint64
	total_PSS_kb = 0

	monitorPtr := flag.Bool("m", false, "Monitor Mode")
	process_namePtr := flag.String("p", "",
		"Process name to measure PSS memory")
	csv_filePtr := flag.String("f", "",
		"File name of CSV to save result")
	flag.Parse()

	if *process_namePtr != "" {
		process_name = *process_namePtr
	}
	if *monitorPtr {
		//TODO implement a thread that monitor every X seconds/ms
		for {
			time.Sleep(time.Duration(delay) * time.Millisecond)
			process_list, total_PSS_kb = scan(process_name)
			print_list(process_list, total_PSS_kb)
		}
		os.Exit(0)
	}

	process_list, total_PSS_kb = scan(process_name)
	print_list(process_list, total_PSS_kb)

	if *csv_filePtr != "" {
		csv_file_name = *csv_filePtr
		write_csv(process_list, csv_file_name)
	}
}
