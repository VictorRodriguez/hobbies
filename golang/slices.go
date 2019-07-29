package main

import "fmt"

func main() {
	s := make([]string, 3)
	fmt.Println("slice=",s)

	s[0] = "hola"
	s[1] = "mundo"
	fmt.Println("slice=",s)

	c := make([]string, len(s))
	copy(c, s)
	fmt.Println("cpy:", c)

}
