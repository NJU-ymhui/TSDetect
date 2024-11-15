import static org.junit.Assert.*;

public class ExampleTest {

    @org.junit.Test
    public void testDuplicateAssertions() {
        assertTrue("Condition should be true", condition1);
        assertTrue("Condition should be true", condition1); // 重复的断言
        assertEquals("Values should be equal", expectedValue, actualValue);
        fail("This test has failed"); // 可能与其他消息重复
        System.out.println();
    }
}