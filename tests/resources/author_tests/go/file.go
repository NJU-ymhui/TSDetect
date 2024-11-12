_, err2 := os.Open("path/to/a.txt")

func TestFileExists(t *testing.T) {
    _, err := os.Stat("example.txt")
    if os.IsNotExist(err) {
        t.Error("File does not exist")
    }
    if err2 != nil {
        t.Error("File does not exist")
    }
}
