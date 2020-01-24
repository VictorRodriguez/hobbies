package main

import (
	"fmt"
	"time"
)

func main() {
	ticker := time.Tick(time.Second)
	fmt.Println("Counting down to launch...")

	for i := 10; i >= 0; i-- {
		<-ticker
		fmt.Printf("\rOn 10/%d", i) // use \r if you are running this in terminal

	}
	fmt.Println("\nWe have lift off!")
}

