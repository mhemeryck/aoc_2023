package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const (
	FILENAME = "input.txt"
	// FILENAME = "example.txt"
)

func parseLineInt(line string) ([]int, error) {
	result := make([]int, 0)
	for _, t := range strings.Split(line, " ") {
		if t != "" {
			tim, err := strconv.Atoi(t)
			if err != nil {
				return result, err
			}
			result = append(result, tim)
		}
	}
	return result, nil
}

func parseLine(line string) (int, error) {
	parsed := strings.ReplaceAll(line, " ", "")
	return strconv.Atoi(parsed)
}

func main() {
	bytes, _ := ioutil.ReadFile(FILENAME)
	LINES := strings.Split(string(bytes), "\n")

	// times
	timeLine := strings.Split(LINES[0], ":")[1]
	times, err := parseLineInt(timeLine)
	if err != nil {
		panic(err)
	}
	// distances
	distanceLine := strings.Split(LINES[1], ":")[1]
	distances, err := parseLineInt(distanceLine)
	if err != nil {
		panic(err)
	}

	// fmt.Printf("%v\n%v\n", times, distances)

	nAccepted := make([]int, 0)
	for k := 0; k < len(times); k++ {
		tMax := times[k]
		dMax := distances[k]
		accepted := make([]int, 0)
		n := 0
		for tInit := 1; tInit < tMax; tInit++ {
			tRem := tMax - tInit
			if tRem <= 0 {
				break
			}
			v := tInit
			d := v * tRem
			if d > dMax {
				accepted = append(accepted, tInit)
				n++
			}
		}
		nAccepted = append(nAccepted, n)
		// fmt.Printf("%v\n", accepted)
	}
	// fmt.Printf("%v\n", nAccepted)

	prod := 1
	for _, n := range nAccepted {
		prod *= n
	}
	fmt.Printf("answer part 1: %d\n", prod)

	// part 2
	tMax, err := parseLine(timeLine)
	if err != nil {
		panic(err)
	}
	dMax, err := parseLine(distanceLine)
	if err != nil {
		panic(err)
	}
	// fmt.Printf("%d - %d\n", tMax, dMax)

	n := 0
	for tInit := 1; tInit < tMax; tInit++ {
		tRem := tMax - tInit
		if tRem <= 0 {
			break
		}
		v := tInit
		d := v * tRem
		if d > dMax {
			n++
		}
	}
	fmt.Printf("answer part 2: %d\n", n)
}
