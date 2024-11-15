public class Example {
    private int unusedField, unusedField2, unusedField3 = 1, unusedField4;
    private int usedField;

    public void setUp() {
        // Setup method
    }

    @Ignored
    public void testMethod() {
        int a = 2, b = 3;
        int c = 2, d = 5, e = 9;
        usedField = 1;
        unusedField = 2;
        unusedField2 = 3;
    }
}