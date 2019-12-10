package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
)

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
			if _, err := strconv.Atoi(f.Name()); err == nil {
				fmt.Println(f.Name())
			}
		}
	}
}
