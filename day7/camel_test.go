package main

import (
	"reflect"
	"testing"
)

func Test_isFiveOfAkind(t *testing.T) {
	if !isFiveOfAKind("AAAAA") {
		t.Error("Expected five of a kind")
	}
	if isFiveOfAKind("ATJ45") {
		t.Error("Expected not five of a kind")
	}
}

func Test_isFourOfAkind(t *testing.T) {
	if !isFourOfAKind("23333") {
		t.Error("Expected four of a kind")
	}
	if isFourOfAKind("ATJ45") {
		t.Error("Expected not four of a kind")
	}
}

func Test_isFullHouse(t *testing.T) {
	if !isFullHouse("TT333") {
		t.Fail()
	}
	if isFullHouse("ATJ45") {
		t.Fail()
	}
}

func Test_isThreeOfAKind(t *testing.T) {
	if !isThreeOfAKind("TTT98") {
		t.Fail()
	}
	if isThreeOfAKind("A234") {
		t.Fail()
	}
	if isThreeOfAKind("TTTT5") {
		t.Fail()
	}
	if !isThreeOfAKind("68J2J") {
		t.Fail()
	}
}

func Test_isTwoPair(t *testing.T) {
	if !isTwoPair("23432") {
		t.Fail()
	}
	if isTwoPair("A234") {
		t.Fail()
	}
}

func Test_isOnePair(t *testing.T) {
	if !isOnePair("A23A4") {
		t.Fail()
	}
	if isOnePair("A234") {
		t.Fail()
	}
}

func Test_countRanks(t *testing.T) {
	testCases := map[string]struct {
		expected map[string]int
		actual   map[string]int
	}{
		"simple": {
			map[string]int{"2": 1, "3": 1, "4": 1, "5": 1, "A": 1},
			countRanksRegular("2345A"),
		},
		"doubles": {
			map[string]int{"2": 2, "4": 1, "Q": 2},
			countRanksRegular("224QQ"),
		},
	}
	for _, testCase := range testCases {
		if !reflect.DeepEqual(testCase.expected, testCase.actual) {
			t.Errorf("Expected %v got ranks, got %v\n", testCase.expected, testCase.actual)
		}
	}
}

func Test_handRanks(t *testing.T) {
	testCases := map[string]struct {
		expected int
		actual   int
	}{
		"five of a kind": {
			FIVE_OF_A_KIND,
			handRank("AAAAA"),
		},
		"four of a kind": {
			FOUR_OF_A_KIND,
			handRank("AA8AA"),
		},
		"full house": {
			FULL_HOUSE,
			handRank("23332"),
		},
		"three of a kind": {
			THREE_OF_A_KIND,
			handRank("TTT98"),
		},
		"two pair": {
			TWO_PAIR,
			handRank("23432"),
		},
		"one pair": {
			ONE_PAIR,
			handRank("A23A4"),
		},
		"high card": {
			HIGH_CARD,
			handRank("23456"),
		},
	}
	for _, testCase := range testCases {
		if testCase.expected != testCase.actual {
			t.Errorf("Expected %v got %v\n", testCase.expected, testCase.actual)
		}
	}
}

func Test_handCmp(t *testing.T) {
	// Five of a kinds wins (left is highest)
	if handCmp(Hand{hand: "AAAAA", bid: 1}, Hand{hand: "23459", bid: 2}) != 1 {
		t.Fail()
	}
	// full house wins (left is highest)
	if handCmp(Hand{hand: "22333", bid: 1}, Hand{hand: "56789", bid: 2}) != 1 {
		t.Fail()
	}
	// four of kind wins (right is highest)
	if handCmp(Hand{hand: "22333", bid: 1}, Hand{hand: "88881", bid: 2}) != -1 {
		t.Fail()
	}
	// four of kind wins; high card (left is highest)
	if handCmp(Hand{hand: "98888", bid: 1}, Hand{hand: "88881", bid: 2}) != 1 {
		t.Fail()
	}
	// completely equal
	if actual := handCmp(Hand{hand: "98888", bid: 1}, Hand{hand: "98888", bid: 2}); actual != 0 {
		t.Errorf("Got %v\n", actual)
	}
	// three of a kind, right wins due to Q
	if handCmp(Hand{hand: "T55J5", bid: 1}, Hand{hand: "QQQJA", bid: 2}) != -1 {
		t.Fail()
	}
}

func Test_countRanksJoker(t *testing.T) {
	testCases := map[string]struct {
		expected map[string]int
		actual   map[string]int
	}{
		"simple": {
			map[string]int{"3": 2, "2": 1, "T": 1, "K": 1},
			countRanks("32T3K"),
		},
		"two pair": {
			map[string]int{"K": 2, "6": 1, "7": 2},
			countRanks("KK677"),
		},
		"four of a kind": {
			map[string]int{"5": 4, "T": 1},
			countRanks("T55J5"),
		},
		"four of a kind 2": {
			map[string]int{"Q": 4, "A": 1},
			countRanks("QQQJA"),
		},
		"full house": {
			map[string]int{"Q": 3, "A": 1, "2": 1},
			countRanks("QQJ2A"),
		},
		"three of a kind": {
			map[string]int{"A": 3, "3": 1, "4": 1},
			countRanks("JJA34"),
		},
		"three of a kind 2": {
			map[string]int{"8": 3, "6": 1, "2": 1},
			countRanks("68J2J"),
		},
	}
	for _, testCase := range testCases {
		if !reflect.DeepEqual(testCase.expected, testCase.actual) {
			t.Errorf("Expected %v got ranks, got %v\n", testCase.expected, testCase.actual)
		}
	}
}

func Test_handRank(t *testing.T) {
	if actual := handRank("59TJJ"); actual != THREE_OF_A_KIND {
		t.Errorf("Expected three of a kind, got %v\n", printRank(actual))
	}
	if actual := handRank("J68J4"); actual != THREE_OF_A_KIND {
		t.Errorf("Expected three of a kind, got %v\n", printRank(actual))
	}
}
