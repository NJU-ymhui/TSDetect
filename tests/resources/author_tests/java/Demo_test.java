public class Demo_test {

    public void helper() {
        Demo d = new Demo();
        d.func();
        d.func();
        d.hello();
    }

    @Test
    public void test1() {
        helper();
        System.out.println("Hello World");
    }

    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}