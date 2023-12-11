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

var (
	AllCards = []string{"2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"}
)

func isFiveOfAKind(hand string) bool {
	for _, count := range countRanks(hand) {
		if count == 5 {
			return true
		}

	}
	return false
}

func isFourOfAKind(hand string) bool {
	for _, count := range countRanks(hand) {
		if count == 4 {
			return true
		}

	}
	return false
}

func isFullHouse(hand string) bool {
	hasRank3 := false
	hasRank2 := false
	for _, count := range countRanks(hand) {
		if count == 3 {
			// at least one with rank 3
			hasRank3 = true
		}
		if count == 2 {
			// at least one with rank 2
			hasRank2 = true

		}
	}
	return hasRank2 && hasRank3

}

func isThreeOfAKind(hand string) bool {
	selected := ""
	for card, count := range countRanks(hand) {
		if count == 3 {
			selected = card
		}
	}
	// no card selected, so no three of a kind
	if selected == "" {
		return false
	} else {
		// there was another higher ranking combination
		for card, count := range countRanks(hand) {
			if card != selected && count >= 3 {
				return false
			}
		}
	}
	return true
}

func isTwoPair(hand string) bool {
	pairCount := 0
	for _, count := range countRanks(hand) {
		if count == 2 {
			pairCount++
		}
	}
	return pairCount == 2
}

func isOnePair(hand string) bool {
	pairCount := 0
	for _, count := range countRanks(hand) {
		if count == 2 {
			pairCount++
		}
	}
	return pairCount == 1
}

func countRanks(hand string) map[string]int {
	result := make(map[string]int, 0)
	for _, s := range AllCards {
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