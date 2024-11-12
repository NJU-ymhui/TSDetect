package main

import (
    "errors"
    "fmt"
)

func doSomething() error {
    return errors.New("an error occurred")
}

func mayPanic() {
    panic("something went wrong") // 使用 panic
}

func main() {
    err := doSomething()
    doSomething()
    doSomething()
    if err != nil {
        fmt.Println("Error:", err)
    }
    mayPanic() // 触发 panic
}
