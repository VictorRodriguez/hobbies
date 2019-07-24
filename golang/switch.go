package main

import "fmt"
import "bufio"
import "os"
import "strconv"
import "log"
import "strings"

func main(){

	i:=2
	reader := bufio.NewReader(os.Stdin)
	text,_:= reader.ReadString('\n')
	text = strings.TrimSuffix(text, "\n")
	i,err:= strconv.Atoi(text)
	if err != nil {
	    log.Fatal(err)
	}

	fmt.Println("Value ",i )
	switch i {
		case 1:
			fmt.Println("one")
		case 2:
			fmt.Println("two")
		case 3:
			fmt.Println("tree")
	}

}
