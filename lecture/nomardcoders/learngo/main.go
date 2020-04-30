package main

import (
	"fmt"
	"strings"

	"github.com/HyungJiny/learngo/mydict"
)

func printAll(words ...string) {
	fmt.Println(words)
}

func lenAndUpper(name string) (int, string) {
	return len(name), strings.ToUpper(name)
}

func multiply(a, b int) int {
	return a * b
}

func main() {
	dictionary := mydict.Dictionary{}
	baseWord := "hello"
	dictionary.Add(baseWord, "First")
	dictionary.Search(baseWord)
	dictionary.Delete(baseWord)
	word, err := dictionary.Search(baseWord)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(word)
	}
}
