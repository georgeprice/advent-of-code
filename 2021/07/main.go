package main

import (
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func solve(raw string) int {
	values := make([]int, 0, 256)
	limit := 0
	for _, raw := range strings.Split(raw, ","){
		value, _ := strconv.Atoi(raw)
		values = append(values, value)
		if value > limit {
			limit = value
		}
	}
	lowest := -1
	for to := 0; to < limit; to++ {
		total := 0
		for j := 0; j < len(values); j++ {
			from := values[j]
			diff := abs(to - from)
			total += cost(diff)
		}
		if lowest == -1 || total < lowest {
			lowest = total
		}
	}
	return lowest
}

func abs(in int) int {
	if in < 0 {
		return -in
	}
	return in
}

var cache = map[int]int{}
func cost(distance int) int {
	_, cached := cache[distance]
	if cached {
		return cache[distance]
	}
	var result int
	if distance > 0 {
		result = distance + cost(distance - 1)
	}
	cache[distance] = result
	return result
}

func main() {
	bs, err := ioutil.ReadFile("2021/07/in")
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	log.Printf("out: %d", solve(string(bs)))
}
