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

func Test_countRanks(t *testing.T) {
	expected := map[string]int{"2": 2, "3": 3, "4": 4, "5": 5, "A": 1}
	actual := countRanks("2345A")
	if !reflect.DeepEqual(actual, expected) {
		t.Errorf("Expected matching count ranks, got %v\n", actual)
	}
}
