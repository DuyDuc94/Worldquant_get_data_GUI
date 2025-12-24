/*
 * DuyDuc94
 */

import java.util.*;

/**
 *
 * @author duy20
 */
public class Core_ProcessData {

    static LinkedList<String> Keyword = new LinkedList<>();
    static LinkedList<String> Type = new LinkedList<>();

    public Core_ProcessData() {
        Type.add("vector");
        Type.add("matrix");
        Type.add("group");
    }

    public String inputKeyword(String inputString) {
        Keyword.clear();
        String[] recogs = inputString.split(" ");
        Keyword.addAll(Arrays.asList(recogs));
        Object[] keys = Keyword.toArray();
        String result = "";
        for (Object key : keys) {
            result += key + ", ";
        }
        return result.substring(0, result.length() - 2) + "\n";
    }

    public static String getKeywords() {
        Object[] keys = Keyword.toArray();
        String result = "";
        for (Object key : keys) {
            result += key + ", ";
        }
        return result.substring(0, result.length() - 2) + "\n";
    }
    
    public static String getTypes() {
        Object[] types = Type.toArray();
        String result = "";
        for (Object type : types) {
            result += type + ", ";
        }
        return result.substring(0, result.length() - 2) + "\n";
    }

    public boolean detectKeyword(String data) {
        Object[] keys = Keyword.toArray();
        for (Object key : keys) {
            if (data.startsWith((String) key)) {
                return true;
            }
        }
        return false;
    }

    public boolean detectType(String data) {
        Object[] types = Type.toArray();
        for (Object type : types) {
            if (data.compareTo((String) type) == 0) {
                return true;
            }
        }
        return false;
    }
}
