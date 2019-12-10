package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
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
	var directory string
	directory = "/proc/"
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		log.Fatal(err)
	}

	for _, f := range files {
		if f.IsDir() {
			if pid, err := strconv.Atoi(f.Name()); err == nil {
				p := process{pid: pid}
				p.PSS_kb = 0

				dat, err := ioutil.ReadFile(directory + f.Name() + "/comm")
				check(err)
				p.name = strings.TrimSuffix(string(dat), "\n")

				file, err := os.Open(directory + f.Name() + "/smaps")
				if err != nil {
					log.Fatal(err)
				}
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

				fmt.Println(p.name, " PID: ", p.pid, " = ", p.PSS_kb)
			}
		}
	}
}
