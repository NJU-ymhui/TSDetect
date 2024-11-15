import static org.junit.Assert.*;

public class ExampleTest {

    @org.junit.Test
    public void testMultipleProductionMethodCalls() {
        methodA(); // 生产方法调用
        methodB(); // 另一个生产方法调用
        assertTrue("Condition should be true", condition);
    }

    // 生产方法示例
    private void methodA() {
        // 逻辑
    }

    private void methodB() {
        // 逻辑
    }
}
