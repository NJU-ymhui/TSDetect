public class Demo_test {
    @Test
    public void test1() {
        Demo d = new Demo();
        d.func();
        d.func();
        d.hello();
        System.out.println("Hello World");
    }

    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}