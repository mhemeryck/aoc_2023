package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"slices"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	FILENAME = "input.txt"
	// FILENAME = "input2.txt"
	NWORKERS = 8
)

var (
	wg sync.WaitGroup
	mc MinContainer
)

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

func apply(seed int, m []Map) int {
	for _, mp := range m {
		if seed >= mp.Source && seed <= mp.Source+mp.Length {
			return mp.Target + (seed - mp.Source)
		}
	}
	return seed

}

func locationForSeed(seed int, m [][]Map) int {
	for _, mp := range m {
		seed = apply(seed, mp)
	}
	return seed
}

func produce(seedRanges []SeedRange, msgs chan<- int) {
	defer wg.Done()
	var prodWg sync.WaitGroup
	for _, seedRange := range seedRanges {
		// fmt.Printf("Start job %d\n", i)
		wg.Add(1)
		prodWg.Add(1)
		sd := seedRange
		go func() {
			defer wg.Done()
			defer prodWg.Done()
			for seed := sd.Offset; seed < sd.Offset+sd.Length; seed++ {
				msgs <- seed
			}
		}()
	}
	prodWg.Wait()
	// ensure we close off the channel ...
	close(msgs)
}

func consume(msgs <-chan int, maps [][]Map) {
	defer wg.Done()

	for i := 0; i < NWORKERS; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for seed := range msgs {
				// fmt.Printf("%v\n", <-msgs)
				location := locationForSeed(seed, maps)
				mc.Check(location)
			}
		}()
	}
}

type Map struct {
	Source int
	Target int
	Length int
}

type SeedRange struct {
	Offset int
	Length int
}

type MinContainer struct {
	mu    sync.Mutex
	Value int
}

func (m *MinContainer) Check(value int) {
	defer m.mu.Unlock()
	m.mu.Lock()
	if value < m.Value {
		m.Value = value
		fmt.Printf("New minimum! %d\n", value)
	}
}

func NewMinContainer() MinContainer {
	return MinContainer{
		Value: math.MaxInt64,
	}
}

func RemapSeeds(seeds []int) []SeedRange {
	var offset int
	result := make([]SeedRange, len(seeds)/2)
	for k, seed := range seeds {
		if k%2 == 0 {
			offset = seed
		} else {
			result = append(result, SeedRange{Offset: offset, Length: seed})
		}
	}
	return result
}

func main() {
	// read lines
	bytes, _ := ioutil.ReadFile(FILENAME)
	fileContent := string(bytes)
	LINES := strings.Split(fileContent, "\n")

	// seeds
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

	// maps
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
			currentMapList = append(currentMapList, Map{Target: t, Source: s, Length: l})

		}
	}
	// fmt.Printf("%v", maps)

	results := make([]int, 0)
	for _, seed := range seeds {
		location := locationForSeed(seed, maps)
		results = append(results, location)
	}

	// fmt.Printf("%v\n", results)
	min := slices.Min(results)
	// part 1
	fmt.Printf("min value: %v\n", min)

	// part 2
	seedRanges := RemapSeeds(seeds)

	var msgs = make(chan int)
	mc = NewMinContainer()

	fmt.Printf("start: %v\n", time.Now())
	wg.Add(1)
	go produce(seedRanges, msgs)
	wg.Add(1)
	go consume(msgs, maps)

	wg.Wait()
	fmt.Printf("the minimum is %v\n", mc.Value)
	fmt.Printf("stop: %v\n", time.Now())

}
