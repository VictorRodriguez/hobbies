package main

import "fmt"

func main(){
	nums := []int{2, 3, 4}
	sum := 0
	for _, num := range nums {
		fmt.Println("num = ",num)
		sum += num
	}
	fmt.Println("sum = ",sum)
}
