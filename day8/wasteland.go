package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strings"
)

const (
	FILENAME = "input.txt"
	// FILENAME = "example.txt"
	// FILENAME = "example2.txt"
)

var (
	pattern = regexp.MustCompile(`(\w{3}) = \((\w{3}), (\w{3})\)`)
	START   = Point("AAA")
	END     = Point("ZZZ")
)

type Point string

type Edge struct {
	Left  Point
	Right Point
}

func main() {
	// parse
	bytes, _ := ioutil.ReadFile(FILENAME)
	LINES := strings.Split(string(bytes), "\n")

	directions := LINES[0]
	points := make(map[Point]Edge, 0)
	for _, line := range LINES {
		matches := pattern.FindAllStringSubmatch(line, -1)

		if matches == nil {
			continue
		}

		match := matches[0]
		if len(match[0]) >= 4 {
			p := Point(match[1])
			l := Point(match[2])
			r := Point(match[3])
			// fmt.Printf("%v - %v - %v\n", p, l, r)
			points[p] = Edge{Left: l, Right: r}
		}
	}
	// fmt.Printf("points %v\n", points)

	count := 0
	var point = START
	for point != END {
		for _, d := range directions {
			if string(d) == "L" {
				point = points[point].Left
			} else if string(d) == "R" {
				point = points[point].Right
			} else {
				panic("unexpected direction")
			}
			count++
		}
	}
	fmt.Printf("part 1: %v\n", count)
}
