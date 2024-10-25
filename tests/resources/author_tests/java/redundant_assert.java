import org.junit.Test;
import static org.junit.Assert.*;

public class ExampleTest {

    // 冗余断言 + 断言轮盘 + 默认测试
    @Test
    public void testRedundantAssertions() {
        int expectedValue = 5;
        int actualValue = 5;

        System.out.println("start!");

        // 这个断言是冗余的，因为它实际上在比较相同的值
        assertEquals(expectedValue, actualValue);

        // 冗余的单参数断言
        assertTrue(true); // 这是冗余的，因为它总是为真
        assertFalse(false); // 也是冗余的，因为它总是为假

        // 这个断言也是冗余的
        assertNull(null); // 这是冗余的，因为它总是为null
    }
}
