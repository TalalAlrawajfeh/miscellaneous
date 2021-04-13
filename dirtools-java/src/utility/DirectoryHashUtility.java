package utility;

import exceptions.UtilityException;
import pool.thread.ThreadPool;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static utility.FileHashUtility.getFileHashCode;

/**
 * Created by u624 on 5/6/17.
 */
public class DirectoryHashUtility {
    private ThreadPool threadPool;
    private Path directoryPath;

    public DirectoryHashUtility(Path directoryPath, boolean multithreaded, int threadCount) {
        validateDirectoryPath(directoryPath);
        validateThreadsCount(multithreaded, threadCount);
        this.directoryPath = directoryPath;
        if (multithreaded) {
            threadPool = new ThreadPool(threadCount);
        }
    }

    public Map<Path, String> getHashTable() {
        try {
            Map<Path, String> hashTable = Collections.synchronizedMap(new HashMap<>());
            Files.walk(directoryPath)
                    .filter(p -> p.toFile().isFile())
                    .forEach(p -> threadPool.take().doOperation(() -> hashTable.put(p, getFileHashCode(p))));
            return hashTable;
        } catch (IOException e) {
            throw new UtilityException(e);
        } finally {
            threadPool.closeAllResources();
        }
    }

    private void validateThreadsCount(boolean multithreaded, int threadsCount) {
        if (!multithreaded && threadsCount != 0 || multithreaded && threadsCount <= 0) {
            throw new UtilityException("threadsCount parameter must be zero if not multithreaded");
        }
    }

    private void validateDirectoryPath(Path directoryPath) {
        if (!directoryPath.toFile().isDirectory()) {
            throw new UtilityException(directoryPath + " is not a path of a directory");
        }
    }
}
