package main;

import utility.DirectoryHashUtility;

import java.io.BufferedWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

/**
 * Created by u624 on 5/6/17.
 */
public class DirTools {
    private DirTools() {
        /* static class */
    }

    public static void main(String[] args) throws Exception {
        String firstPath = "/Talal/Google Drive Harvard QE";
        String secondPath = "/Talal/Talal's Folder Harvard QE";

        Map<Path, String> hashTable1 =
                new DirectoryHashUtility(Paths.get(firstPath),
                        true, 10).getHashTable();

        Map<Path, String> hashTable2 =
                new DirectoryHashUtility(Paths.get(secondPath),
                        true, 10).getHashTable();

        List<String> differences1 = new ArrayList<>();
        Thread thread1 = new Thread(() -> {
            for (Entry<Path, String> entry : hashTable1.entrySet()) {
                if (!hashTable2.values().contains(entry.getValue())) {
                    differences1.add(entry.getKey().toString());
                }
            }
        });
        thread1.start();

        List<String> differences2 = new ArrayList<>();
        Thread thread2 = new Thread(() -> {
            for (Entry<Path, String> entry : hashTable2.entrySet()) {
                if (!hashTable1.values().contains(entry.getValue())) {
                    differences2.add(entry.getKey().toString());
                }
            }
        });
        thread2.start();

        thread1.join();
        thread2.join();

        try (BufferedWriter bufferedWriter = Files.newBufferedWriter(Paths.get("/home/u624/Desktop/results.txt"))) {
            bufferedWriter.write("Detected files in " + firstPath + ":\n\n");
            for (String diff : differences1) {
                bufferedWriter.write(diff + "\n\n");
            }
            bufferedWriter.write("\n\n=====================================================\n\n");
            bufferedWriter.write("Detected files in " + secondPath + ":\n\n");
            for (String diff : differences2) {
                bufferedWriter.write(diff + "\n\n");
            }
        }
    }
}

