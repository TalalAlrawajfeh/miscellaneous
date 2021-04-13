package utility;

import exceptions.UtilityException;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Created by u624 on 5/6/17.
 */
public class FileHashUtility {
    public static final int HEX_RADIX = 16;
    private static int DEFAULT_BUFFER_SIZE = 8192;
    private static final String MD5_HASH_ALGORITHM = "MD5";
    private static final String ZERO_PAD = "0";

    public static String getFileHashCode(Path filePath) {
        validateFilePath(filePath);
        String hashCode;
        try (InputStream inputStream = Files.newInputStream(filePath)) {
            MessageDigest messageDigest = MessageDigest.getInstance(MD5_HASH_ALGORITHM);
            int bytesRead;
            byte[] buffer = new byte[DEFAULT_BUFFER_SIZE];
            while (-1 != (bytesRead = inputStream.read(buffer))) {
                messageDigest.update(buffer, 0, bytesRead);
            }
            hashCode = convertByteArrayToHexString(messageDigest.digest());
        } catch (NoSuchAlgorithmException | IOException e) {
            throw new UtilityException(e);
        }
        return hashCode;
    }

    private static void validateFilePath(Path filePath) {
        if (!filePath.toFile().isFile()) {
            throw new UtilityException(filePath + " is not a path to a file");
        }
    }

    private static String convertByteArrayToHexString(byte[] byteArray) {
        StringBuilder hexString = new StringBuilder();
        for (byte value : byteArray) {
            hexString.append(getHexCode(value));
        }
        return hexString.toString();
    }

    private static String getHexCode(byte value) {
        String hexCode = Integer.toString(Byte.toUnsignedInt(value), HEX_RADIX);
        if (1 == hexCode.length()) {
            hexCode = ZERO_PAD + hexCode;
        }
        return hexCode;
    }
}
