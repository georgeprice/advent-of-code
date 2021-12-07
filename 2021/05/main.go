package main

import (
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type coordinate struct{ x, y int }

func parseCoordinate(raw string) coordinate {
	values := strings.Split(raw, ",")
	rawX, rawY := values[0], values[1]
	x, _ := strconv.Atoi(rawX)
	y, _ := strconv.Atoi(rawY)
	return coordinate{x: x, y: y}
}

type grid [][]int

func newGrid(width, height int) *grid {
	g := make(grid, 0, height + 1)
	for y := 0; y < height + 1; y++ {
		g = append(g, make([]int, width + 1))
	}
	return &g
}

func (g *grid) draw(from, to coordinate) {
	xDiff, yDiff := to.x - from.x, to.y - from.y
	xChange := 0
	switch {
	case xDiff < 0:
		xChange = -1
	case xDiff > 0:
		xChange = 1
	}
	yChange := 0
	switch {
	case yDiff < 0:
		yChange = -1
	case yDiff > 0:
		yChange = 1
	}
	x, y := from.x, from.y
	for x != to.x || y != to.y {
		(*g)[y][x] += 1
		x, y = x + xChange, y + yChange
	}
	(*g)[to.y][to.x] += 1
}

func (g grid) score() int {
	score := 0
	for _, row := range g {
		for _, cell := range row {
			if cell > 1 {
				score += 1
			}
		}
	}
	return score
}

func solve(raw string) (int, error) {
	lines := strings.Split(raw, "\r\n")

	width, height := 0, 0

	type pair struct { from, to coordinate }
	pairs := make([]pair, 0, len(lines))
	for _, line := range lines {
		if line == "" {
			continue
		}
		rawPairs := strings.Split(line, " -> ")
		fromRaw, toRaw := rawPairs[0], rawPairs[1]

		// parsing starting coordinates, updating width and height of grid
		from := parseCoordinate(fromRaw)
		if from.x > width {
			width = from.x
		}
		if from.y > height {
			height = from.y
		}

		// parsing ending coordinates, updating width and height of grid
		to := parseCoordinate(toRaw)
		if to.x > width {
			width = to.x
		}
		if to.y > height {
			height = to.y
		}
		pairs = append(pairs, pair{from: from, to: to})
	}

	_grid := newGrid(width, height)
	for _, pair := range pairs {
		_grid.draw(pair.from, pair.to)
	}
	return _grid.score(), nil
}

func main() {
	bs, err := ioutil.ReadFile("2021/05/in")
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	in := string(bs)
	score, err := solve(in)
	if err != nil {
		log.Fatalf("err: %s", err)
	}
	log.Printf("score: %d", score)
}
