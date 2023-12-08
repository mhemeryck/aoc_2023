package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const FILENAME = "input.txt"

// var LINES string = `seeds: 79 14 55 13

// seed-to-soil map:
// 50 98 2
// 52 50 48

// soil-to-fertilizer map:
// 0 15 37
// 37 52 2
// 39 0 15

// fertilizer-to-water map:
// 49 53 8
// 0 11 42
// 42 0 7
// 57 7 4

// water-to-light map:
// 88 18 7
// 18 25 70

// light-to-temperature map:
// 45 77 23
// 81 45 19
// 68 64 13

// temperature-to-humidity map:
// 0 69 1
// 1 0 69

// humidity-to-location map:
// 60 56 37
// 56 93 4`

type Map struct {
	source int
	target int
	length int
}

func main() {
	bytes, _ := ioutil.ReadFile(FILENAME)
	fileContent := string(bytes)
	LINES := strings.Split(fileContent, "\n")

	seedLine := strings.Split(string(LINES[0]), ":")[1]
	seeds := make([]int, 0)

	for _, s := range strings.Split(seedLine, " ") {
		if s != "" {
			seed, err := strconv.Atoi(s)
			if err != nil {
				panic(err)
			}
			seeds = append(seeds, seed)
		}
	}

	maps := make([][]Map, 0)
	var currentMapList []Map
	for _, line := range LINES[1:] {
		if strings.Contains(line, "map") {
			currentMapList = make([]Map, 0)
		} else if line == "" || line == "\n" {
			if len(currentMapList) != 0 {
				maps = append(maps, currentMapList)
			}
		} else {
			lineSplit := strings.Split(line, " ")
			target := lineSplit[0]
			source := lineSplit[1]
			length := lineSplit[2]
			t, _ := strconv.Atoi(target)
			s, _ := strconv.Atoi(source)
			l, _ := strconv.Atoi(length)
			currentMapList = append(currentMapList, Map{target: t, source: s, length: l})

		}
		fmt.Println(line)
	}

	fmt.Printf("%v", maps)
}
