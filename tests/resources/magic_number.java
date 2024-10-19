import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class ExampleTest {

    @Test
    public void testMagicNumber() {
        int result = add(5, 10); // 这里的5和10是魔法数字
        int ans = 15;
        assertEquals(15, result);
    }

    private int add(int a, int b) {
        return a + b;
    }
}