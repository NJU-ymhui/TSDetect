public class ControlStructures {
    public static void main(String[] args) {
        int number = 5;

        // if
        if (number > 0) System.out.println("Positive");

        // for
        for (int i = 1; i <= 5; i++) System.out.print(i + " ");

        // switch
        switch (number) {
            case 5: System.out.println("\nFive"); break;
            default: System.out.println("\nNot five");
        }

        // foreach
        for (String fruit : new String[]{"Apple", "Banana", "Cherry"}) {
            System.out.print(fruit + " ");
        }

        // while
        int count = 0;
        while (count < 3) System.out.print(count++ + " ");
    }
}