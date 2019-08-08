package main

import "fmt"

func add(value_a,value_b int) int {
	return value_a + value_b
}

func foo(){
	fmt.Println("hi there from foo")
}

func main(){
	fmt.Println("hi there")
	foo()
	fmt.Println(add(2,3))
}
