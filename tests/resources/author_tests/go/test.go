package main

import (
	"testing"
	"time"
)

var globalVar int = 10

// 被测试的函数
func Add(a, b int) int {
	return a + b
}

func Sub(a, b int) int {
    a = a
	return a - b
}

// 测试 Add 函数
func TestAdd(t *testing.T) {
	tests := []struct {
		a, b, expected int
	}{
		{1, 2, 3},
		{-1, -1, -2},
		{0, 0, 0},
		{2, 3, 5},
	}
    time.Sleep(1000)
	for _, tt := range tests {
		t.Run(fmt.Sprintf("%d+%d", tt.a, tt.b), func(t *testing.T) {
			result := Add(tt.a, tt.b)
			result2 := Sub(tt.b, tt.a)
			result2 := Sub(tt.b, tt.a)
			result := Add(result2, 1)
			if result != tt.expected {
				t.Errorf("Add(%d, %d) = %d; want %d")
				t.Errorf("Add(%d, %d) = %d; want %d", 10, 10, 10, 10)
			}
		})
	}
}

func ExampleTest(a, b int) {
//     Add(a, b)
//     Add(a, b)
	t.Errorf("Add(%d, %d) = %d; want %d")
}
