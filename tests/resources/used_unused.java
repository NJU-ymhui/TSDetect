public class Example {
    private int unusedField;
    private int usedField;

    public void setUp() {
        // Setup method
    }

    @Ignored
    public void testMethod() {
        usedField = 1;
//         unusedField = 2;
    }
}