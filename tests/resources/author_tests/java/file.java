import org.junit.Test;
import java.io.File;

import static org.junit.Assert.assertTrue;

public class FileTest {

    private File testFile = new File("test.txt"), testFile2 = new File("test2.txt");

    void func() {}

    @Test
    public void testFileOperations(File a, int b) {
        // 首先检查文件是否存在
        if (!testFile.exists() && testFile2.exists() && a.exists()) {
            // 可以选择创建文件或直接抛出异常
            // assertTrue("File does not exist.", testFile.createNewFile());
            System.out.println("File does not exist. Creating a new file.");
            assertTrue(testFile.createNewFile());
        }
//         File other = new File("test2.txt");
        // 确保文件存在后，再进行其他操作
        assertTrue("File is not a regular file.", testFile.isFile());
        System.out.println("Performing operations on the file...");
    }

//     @Test
//     public void testFileOperations2() {
//         File t = new File("test.txt")
//         t.close();
//     }
}
