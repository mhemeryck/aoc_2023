package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"slices"
	"strings"
)

const (
	FILENAME = "input.txt"
	// FILENAME = "example.txt"
	// FILENAME = "example2.txt"
	// FILENAME = "example3.txt"
)

var (
	pattern = regexp.MustCompile(`(\w{3}) = \((\w{3}), (\w{3})\)`)
	START   = Point("AAA")
	END     = Point("ZZZ")
)

func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// find Least Common Multiple (LCM) via GCD
func LCM(a, b int, integers ...int) int {
	result := a * b / GCD(a, b)

	for i := 0; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

type Point string

type Edge struct {
	Left  Point
	Right Point
}

func countHops(start Point, endPoints []Point, points map[Point]Edge, directions string) int {
	count := 0
	var point Point = start
	for !slices.Contains(endPoints, point) {
		for _, d := range directions {
			if string(d) == "L" {
				point = points[point].Left
			} else if string(d) == "R" {
				point = points[point].Right
			} else {
				panic("unexpected direction")
			}
			// fmt.Printf("-> %v ", point)
			count++
		}
	}
	fmt.Printf("We've hit an endpoint! %v\n", point)
	return count
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

	// count := 0
	// var point = START
	// for point != END {
	// 	for _, d := range directions {
	// 		if string(d) == "L" {
	// 			point = points[point].Left
	// 		} else if string(d) == "R" {
	// 			point = points[point].Right
	// 		} else {
	// 			panic("unexpected direction")
	// 		}
	// 		count++
	// 	}
	// }
	// count := countHops(START, []Point{END}, points, directions)
	// fmt.Printf("part 1: %v\n", count)

	// part2
	startNodes := make([]Point, 0)
	endNodes := make([]Point, 0)
	for key := range points {
		if strings.HasSuffix(string(key), "A") {
			startNodes = append(startNodes, key)
		} else if strings.HasSuffix(string(key), "Z") {
			endNodes = append(endNodes, key)
		}
	}

	counts := make([]int, len(startNodes))
	for k, point := range startNodes {
		fmt.Printf("start node: %v\n", point)
		counts[k] = countHops(point, endNodes, points, directions)

	}

	fmt.Printf("count  %v\n", counts)
	result := LCM(counts[0], counts[1], counts[2:]...)
	fmt.Printf("part 2: %v\n", result)
}
