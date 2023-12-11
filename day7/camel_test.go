package main

import "testing"

func test_isFiveOfAkind(t *testing.T) {
	if !isFiveOfAKind("AAAAA"){
		t.Error("Expected five of a kind")
	}
}
