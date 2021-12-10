package main

import (
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type lookup struct { age, days int }
var cache = make(map[lookup]int)
func _solver(age, days int) int{
	key := lookup{ age, days }
	_, cached := cache[key]
	switch {
	case cached:
	case days < 1, age > days:
		cache[key] = 1
	case age == 0:
		cache[key] = _solver(6, days - 1) + _solver(8, days - 1)
	default:
		cache[key] = _solver(0, days - age)
	}
	return cache[key]
}

func solve(raw string, days int) int {
	result := 0
	for _, raw := range strings.Split(raw, ",") {
		value, _ := strconv.Atoi(raw)
		result += _solver(value, days)
	}
	return result
}

func main() {
	bs, err := ioutil.ReadFile("2021/06/in")
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	in, days := string(bs), 256
	out := solve(in, days)
	log.Printf("result: %d", out)
}
