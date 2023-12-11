package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const (
	// FILENAME = "input.txt"
	FILENAME = "example.txt"

	HIGH_CARD = iota
	ONE_PAIR
	TWO_PAIR
	THREE_OF_A_KIND
	FULL_HOUSE
	FOUR_OF_A_KIND
	FIVE_OF_A_KIND
)

func isFiveOfAKind(hand string) bool {
	firstCard := rune(hand[0])
	for _, h := range hand {
		if h != firstCard {
			return false
		}

	}
	return true
}

func isFourOfAKind(hand string) bool {
	return false
}

func countRanks(hand string) map[string]int {
	result := make(map[string]int, 0)
	for _, s := range []string{"2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"} {
		for _, c := range hand {
			if s == string(c) {
				result[s]++
			}
		}
	}
	return result
}

func main() {
	// parse stuff
	bytes, _ := ioutil.ReadFile(FILENAME)
	LINES := strings.Split(string(bytes), "\n")

	hands := make([]string, len(LINES))
	bids := make([]int, len(LINES))
	for k, line := range LINES {
		if line == "" {
			break
		}
		lineSplit := strings.Split(line, " ")
		hands[k] = lineSplit[0]
		n, err := strconv.Atoi(lineSplit[1])
		if err != nil {
			panic(err)
		}
		bids[k] = n
	}
	fmt.Printf("%v - %v\n", hands, bids)

	_ = make([]string, len(hands))
}
