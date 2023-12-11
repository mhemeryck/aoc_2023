package main

import "testing"

func Test_isFiveOfAkind(t *testing.T) {
	if !isFiveOfAKind("AAAAA") {
		t.Error("Expected five of a kind")
	}
	if isFiveOfAKind("ATJ45") {
		t.Error("Expected not five of a kind")
	}
}
