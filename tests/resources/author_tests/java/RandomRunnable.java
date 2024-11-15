public class RandomRunnable implements Runnable {
    @Override
    public void run() {
        Random random = new Random();
        int randomInt = random.nextInt(100);
        System.out.println("Random Integer from Thread " + Thread.currentThread().getName() + ": " + randomInt);
    }

    public static void main(String[] args) {
        Thread thread1 = new Thread(new RandomRunnable());
        Thread thread2 = new Thread(new RandomRunnable());

        thread1.start();
        thread2.start();
    }
}
