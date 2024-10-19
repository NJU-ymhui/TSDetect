public class Person {
    private String name;

    // 构造函数
    public Person(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public static void main(String[] args) {
        Person person = new Person("Alice");
        System.out.println("Name: " + person.getName());
    }
}
