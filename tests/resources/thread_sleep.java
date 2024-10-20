import org.junit.Test;

public class MyTests {

    @Test
    public void testWithSleep() throws InterruptedException {
        // 使用 Thread.sleep 使测试变得不稳定
        Thread.sleep(1000);
        // 测试逻辑
        assertTrue(true);
    }
}
