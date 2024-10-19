@Test
public void testDivision() {
    int a = 10;
    int b = 0;

    // 使用 assert 来验证不应该出现异常
    try {
        divide(a, b);
        fail("应抛出异常，但没有抛出");
    } catch (ArithmeticException e) {
        // 异常抛出，测试通过
        fail();
    }
    if (b > 0) {
        fail("?");
    }
}

public int divide(int x, int y) {
    return x / y; // 这里可能抛出 ArithmeticException
}
