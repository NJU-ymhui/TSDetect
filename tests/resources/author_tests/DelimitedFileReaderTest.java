import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

public class DelimitedFileReaderTest {

    private File testFile;

    @Before
    public void setUp() throws IOException {
        testFile = File.createTempFile("test", ".txt");
        FileWriter writer = new FileWriter(testFile);
        writer.write("value1,value2,value3\
value4,value5,value6");
        writer.close();
    }

    @After
    public void tearDown() {
        testFile.delete();
    }

    @Test
    public void testHasNext() throws FileNotFoundException {
        DelimitedFileReader reader = new DelimitedFileReader(testFile);
        assertTrue(reader.hasNext());
        reader.next();
        assertTrue(reader.hasNext());
        reader.next();
        assertFalse(reader.hasNext());
    }

    @Test
    public void testNext() throws FileNotFoundException {
        DelimitedFileReader reader = new DelimitedFileReader(testFile);
        assertArrayEquals(new String[]{"value1", "value2", "value3"}, reader.next());
        assertArrayEquals(new String[]{"value4", "value5", "value6"}, reader.next());
        assertThrows(NoSuchElementException.class, () -> reader.next());
    }

    @Test
    public void testRemove() throws FileNotFoundException {
        DelimitedFileReader reader = new DelimitedFileReader(testFile);
        assertThrows(UnsupportedOperationException.class, () -> reader.remove());
    }
}
