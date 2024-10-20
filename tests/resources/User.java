public class User {
    private String name;

    public User(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

//     public static void main(String[] args) {
//         User user1 = new User("Alice");
//         User user2 = new User("Bob");
//
//         // 这里的比较直接调用了 toString 方法, 触发smell
//         if (user1.toString().equals(user2.toString())) {
//             System.out.println("Users are equal");
//         } else {
//             System.out.println("Users are not equal");
//         }
//     }

    public static void main(String[] args) {
        User user1 = new User("Alice");
        User user2 = new User("Bob");

        // 使用具体的属性进行比较，没有 bad smell
        if (user1.getName().equals(user2.getName())) {
            System.out.println("Users are equal");
        } else {
            System.out.println("Users are not equal");
        }
    }
}
