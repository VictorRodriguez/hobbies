package main

import "fmt"

func main(){

	var array[10]int

	fmt.Println(array[1])
	fmt.Println(array)
	fmt.Println(len(array))

	for i:= 0;i < 10; i++{
		array[i] = i
	}

	fmt.Println(array)
}

