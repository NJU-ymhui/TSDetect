public class Example {
    private int unusedField, unusedField2;
    private int usedField;

    public void setUp() {
        // Setup method
    }

    @Ignored
    public void testMethod() {
        int a = 2, b = 3;
        usedField = 1;
        unusedField = 2;
        unusedField2 = 3;
    }
}