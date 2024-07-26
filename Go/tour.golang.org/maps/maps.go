package main

import (
	"fmt"
	"strings"
	"golang.org/x/tour/wc"
)

func WordCount(s string) map[string]int {
	//map["bidule":2 "truc":3]

	//See https://golang.org/pkg/strings/#Fields
	var str_array = strings.Fields(s)
	myMap := make(map[string]int)
	for i := range str_array {
		myMap[str_array[i]]+=1
		fmt.Printf("Mot %d: %s\n", i, str_array[i])
	}
	return myMap
}

func main() {
	wc.Test(WordCount)
}