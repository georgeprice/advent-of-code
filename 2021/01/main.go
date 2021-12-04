package main

import (
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func solve(in string) (int, error) {

	// parse input into array of numbers
	split := strings.Split(in, "\r\n")
	nums := make([]int, 0, len(split))
	for _, ln := range split {
		if ln == "" {
			continue
		}
		num, err := strconv.Atoi(ln)
		if err != nil {
			return 0, err
		}
		nums = append(nums, num)
	}
	return increases(nums), nil
}

func increases(vs []int) int {
	n := 0
	for i := 1; i < len(vs); i++ {
		if vs[i] > vs[i - 1] {
			n++
		}
	}
	return n
}

func solveSlidingWindow(in string) (int, error) {

	// parse input into array of numbers
	split := strings.Split(in, "\r\n")
	nums := make([]int, 0, len(split))
	for _, ln := range split {
		if ln == "" {
			continue
		}
		num, err := strconv.Atoi(ln)
		if err != nil {
			return 0, err
		}
		nums = append(nums, num)
	}

	// reduce the array of numbers into three-measurement sliding window groups
	reduced := make([]int, 0, len(nums) - 2)
	for i := 0; i < len(nums) - 2; i++ {
		window := nums[i] + nums[i + 1] + nums[i + 2]
		reduced = append(reduced, window)
	}
	return increases(reduced), nil
}

func main() {

	bs, err := ioutil.ReadFile("2021/01/in")
	if err != nil {
		log.Fatalf("err: %s", err)
	}

	in := string(bs)
	out, err := solve(in)
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	log.Printf("result: %d", out)

	out, err = solveSlidingWindow(in)
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	log.Printf("result: %d", out)
}
