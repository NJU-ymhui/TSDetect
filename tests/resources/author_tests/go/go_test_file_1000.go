
package main

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestIsValid(t *testing.T) {
	t.Run("Valid expression", func(t *testing.T) {
		exprStr := "1 + 1"
		expected := true
		actual := IsValid(exprStr)
		assert.Equal(t, expected, actual)
	})

	t.Run("Invalid expression", func(t *testing.T) {
		exprStr := "1 +"
		expected := false
		actual := IsValid(exprStr)
		assert.Equal(t, expected, actual)
	})

	t.Run("Empty expression", func(t *testing.T) {
		exprStr := ""
		expected := false
		actual := IsValid(exprStr)
		assert.Equal(t, expected, actual)
	})
}