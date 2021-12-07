package main

import (
	"io/ioutil"
	"log"
	"strings"
)

func solve(raw string) (int, int, error) {
	lines := strings.Split(raw, "\n")
	lineLength := len(lines[0])

	// initialise starting values for gamma, epsilon, oxygen, scrubber
	gamma, epsilon := "", ""
	oxygenValues, scrubberValues := lines[:], lines[:]

	for col := 0; col < lineLength; col++ {

		// counting numbers of zeroes and ones in the column index
		zeros, ones := 0, 0
		for _, row := range lines {
			if row[col] == '1' {
				ones++
			} else {
				zeros++
			}
		}

		// updating gamma and epsilon values
		most, least := mostCommon(lines, col)
		gamma, epsilon = gamma + most, epsilon + least

		// filtering down oxygen and scrubber values
		mostOxygen, _ := mostCommon(oxygenValues, col)
		oxygenValues = filter(oxygenValues, col, mostOxygen[0])
		_, leastScrubber := mostCommon(scrubberValues, col)
		scrubberValues = filter(scrubberValues, col, leastScrubber[0])

	}
	powerConsumption := binaryStringToInt(gamma) *
		binaryStringToInt(epsilon)

	lifeSupportRating := binaryStringToInt(oxygenValues[0]) *
		binaryStringToInt(scrubberValues[0])

	return powerConsumption, lifeSupportRating, nil
}

func mostCommon(values []string, index int) (string, string) {
	zeros, ones := 0, 0
	for _, value := range values {
		if value[index] == '1' {
			ones++
		} else {
			zeros++
		}
	}
	if zeros > ones {
		return "0", "1"
	}
	return "1", "0"
}

func filter(values []string, index int, want uint8) []string {
	if len(values) == 1 {
		return values
	}
	filtered := make([]string, 0, len(values))
	for _, value := range values {
		if value[index] == want {
			filtered = append(filtered, value)
		}
	}
	return filtered
}

func binaryStringToInt(raw string) int {
	out := 0
	for i := 0; i < len(raw); i++ {
		out = out << 1
		if raw[i] == '0' {
			continue
		}
		out += 1
	}
	return out
}

func main() {

	bs, err := ioutil.ReadFile("2021/03/in")
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	in := string(bs)
	power, life, err := solve(in)
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	log.Printf("got power consumption: %d," +
		"life support: %d", power, life)
}
