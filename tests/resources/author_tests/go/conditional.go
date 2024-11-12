package main

import (
    "fmt"
)

func main() {
    // 条件判断示例：if 语句
    x := 10
    if x > 0 {
        fmt.Println("x is positive")
    } else if x < 0 {
        fmt.Println("x is negative")
    } else {
        fmt.Println("x is zero")
    }

    // 条件判断示例：switch 语句
    day := "Wednesday"
    switch day {
    case "Monday":
        fmt.Println("Start of the week")
    case "Friday":
        fmt.Println("End of the week")
    case "Saturday", "Sunday":
        fmt.Println("Weekend")
    default:
        fmt.Println("Midweek")
    }

    // 循环示例：for 循环
    fmt.Println("Using for loop:")
    for i := 0; i < 5; i++ {
        fmt.Println(i)
    }

    // 使用 for 语句模拟 while
    fmt.Println("Using for as while:")
    j := 0
    for j < 5 {
        fmt.Println(j)
        j++
    }
}
