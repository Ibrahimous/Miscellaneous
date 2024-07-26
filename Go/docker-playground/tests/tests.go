package main

import "fmt"

func test() []string {
	x := []string{"truc", "muche"}
	return x
}
func main() {
	x := test()
	fmt.Println(x)
}
