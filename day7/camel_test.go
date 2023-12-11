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
			countRanks("2345A"),
		},
		"doubles": {
			map[string]int{"2": 2, "4": 1, "Q": 2},
			countRanks("224QQ"),
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
