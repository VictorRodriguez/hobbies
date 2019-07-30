package main

import "fmt"
func main(){

	m := make(map[string]int)
	fmt.Println(m)
	m["k1"] = 1
	m["k2"] = 2
	m["k3"] = 3
	fmt.Println(m)
	fmt.Println(m["k1"])

	n := map[string]int{"foo": 1, "bar": 2}
	fmt.Println("map:", n)

}

