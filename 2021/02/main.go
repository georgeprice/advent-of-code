package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type Coordinates struct{ X, Depth, Aim int }

type Command struct {
	Operation Operation
	Value int
}

func ParseCommand(raw string) (Command, error) {
	words := strings.Split(raw, " ")
	rawOperation, rawValue := words[0], words[1]
	value, err := strconv.Atoi(rawValue)
	if err != nil {
		return Command{}, fmt.Errorf("could not parse command raw value, err: %s", err)
	}
	op := Operation(rawOperation)
	return Command{
		Operation: op,
		Value: value,
	}, nil
}

func (command Command) Apply(coordinates Coordinates) Coordinates {
	switch command.Operation {
	case Forward:
		coordinates.X += command.Value
		coordinates.Depth += coordinates.Aim * command.Value
	case Down:
		coordinates.Aim += command.Value
	case Up:
		coordinates.Aim -= command.Value
	}
	if coordinates.Depth < 0 {
		coordinates.Depth = 0
	}
	return coordinates
}

type Operation string

const (
	Forward Operation = "forward"
	Down    Operation = "down"
	Up      Operation = "up"
)

func solve(raw string) (Coordinates, error) {
	coordinates := Coordinates{}
	lines := strings.Split(raw, "\r\n")
	for _, line := range lines {
		command, err := ParseCommand(line)
		if err != nil {
			return Coordinates{}, err
		}
		coordinates = command.Apply(coordinates)
	}
	return coordinates, nil
}

func main() {

	bs, err := ioutil.ReadFile("2021/02/in")
	if err != nil {
		log.Fatalf("err: %s", err)
	}

	in := string(bs)
	coordinates, err := solve(in)
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	log.Printf("coordinates: %+v (%d)", coordinates, coordinates.X * coordinates.Depth)

}
