class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }
}

public class CalculatorTest {
    private void test1(int a, int b) {
        Calculator.multiply(a, b);
    }

    @Test
    public void testAdd() {
        // lazy test smell
        int a = Calculator.add(2, 3);
        int b = Calculator.multiply(2, 3);
    }

    @Test
    public void testMultiply() {
        // 正常的测试
        int result = Calculator.multiply(2, 3);
        assertEquals(6, result);
    }
}
