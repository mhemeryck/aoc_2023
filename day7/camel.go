package main

import (
	"fmt"
	"io/ioutil"
	"slices"
	"strconv"
	"strings"
)

const (
	FILENAME = "input.txt"
	// FILENAME = "example.txt"

	HIGH_CARD = iota
	ONE_PAIR
	TWO_PAIR
	THREE_OF_A_KIND
	FULL_HOUSE
	FOUR_OF_A_KIND
	FIVE_OF_A_KIND
)

var (
	AllCards      = []string{"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"}
	AllCardsJoker = []string{"J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"}
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

func countRanksJoker(hand string) map[string]int {
	ranks := countRanks(hand)
	if !strings.Contains(hand, "J") {
		return ranks
	}

	maxCard := ""
	maxI := -1
	maxCount := 0
	for card, count := range ranks {
		if card == "J" {
			continue
		}

		iCard := slices.Index(AllCards, string(card))
		if count > maxCount {
			maxCount = count
			maxCard = card
		} else if count == maxCount && iCard > maxI {
			maxCount = count
			maxCard = card
			maxI = iCard
		}
	}

	// nothing changed ...
	if maxCard == "" {
		return ranks
	} else {
		newHand := strings.ReplaceAll(hand, "J", maxCard)
		return countRanks(newHand)
	}
}

func handRank(hand string) int {
	if isFiveOfAKind(hand) {
		return FIVE_OF_A_KIND
	} else if isFourOfAKind(hand) {
		return FOUR_OF_A_KIND
	} else if isFullHouse(hand) {
		return FULL_HOUSE
	} else if isThreeOfAKind(hand) {
		return THREE_OF_A_KIND
	} else if isTwoPair(hand) {
		return TWO_PAIR
	} else if isOnePair(hand) {
		return ONE_PAIR
	} else {
		return HIGH_CARD
	}
}

type Hand struct {
	hand string
	bid  int
}

func handCmp(a, b Hand) int {
	rankA := handRank(a.hand)
	rankB := handRank(b.hand)

	// lower than
	if rankA < rankB {
		return -1
		// higher than
	} else if rankA > rankB {
		return 1
	}

	// if equal at this point, compare the ranks by index
	for k := range a.hand {
		cA := a.hand[k]
		cB := b.hand[k]
		iA := slices.Index(AllCards, string(cA))
		iB := slices.Index(AllCards, string(cB))
		if iA < iB {
			return -1
		} else if iA > iB {
			return 1
		}

	}
	return 0
}

func handCmpJoker(a, b Hand) int {
	rankA := handRank(a.hand)
	rankB := handRank(b.hand)

	// lower than
	if rankA < rankB {
		return -1
		// higher than
	} else if rankA > rankB {
		return 1
	}

	// if equal at this point, compare the ranks by index
	for k := range a.hand {
		cA := a.hand[k]
		cB := b.hand[k]
		iA := slices.Index(AllCards, string(cA))
		iB := slices.Index(AllCards, string(cB))
		if iA < iB {
			return -1
		} else if iA > iB {
			return 1
		}

	}
	return 0
}

func main() {
	// parse stuff
	bytes, _ := ioutil.ReadFile(FILENAME)
	LINES := strings.Split(string(bytes), "\n")

	hands := make([]Hand, len(LINES)-1)
	for k, line := range LINES {
		if line == "" {
			break
		}
		lineSplit := strings.Split(line, " ")
		h := lineSplit[0]
		n, err := strconv.Atoi(lineSplit[1])
		if err != nil {
			panic(err)
		}
		hands[k] = Hand{hand: h, bid: n}
	}

	// fmt.Printf("%v\n", hands)
	// sort in place
	slices.SortFunc(hands, handCmp)
	// fmt.Printf("%v\n", hands)

	// product of rank x bid
	result := 0
	for k, hand := range hands {
		result += (k + 1) * hand.bid
	}

	fmt.Printf("Result part 1: %d\n", result)
}
