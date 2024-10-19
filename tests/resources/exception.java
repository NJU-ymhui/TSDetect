@Test
public void testExample() throw Exception{
    try {
        methodThatThrowsException();
    } catch (Exception e) {
        // 捕获异常，可能会触发气味
    }
}
