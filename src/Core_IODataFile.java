/*
 * DuyDuc94
 */


import java.awt.Desktop;
import java.io.File;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 *
 * @author duy20
 */
public class Core_IODataFile {

    String region;
    String rootPath;
    String outputPath;
    String rawDataPath;
    String bufferDataPath;
    String matrixPath;
    String vectorPath;
    String groupPath;

    public Core_IODataFile() {
        region = "USA";
        rootPath = System.getProperty("user.dir");
        outputPath = rootPath + "\\Output";
        rawDataPath = rootPath + "\\RawText\\RawData.txt";
        bufferDataPath = rootPath + "\\RawText\\BufferData.txt";
        matrixPath = outputPath + "\\" + region + "_matrix.txt";
        vectorPath = outputPath + "\\" + region + "_vector.txt";
        groupPath = outputPath + "\\" + region + "_group.txt";
    }

    public String getRegion() {
        return region;
    }

    public String getRawDataPath() {
        return rawDataPath;
    }

    public String getOutputPath() {
        return outputPath;
    }
    
    public String switchRegion(String region) {
        this.region = region;
        matrixPath = rootPath + "\\Output\\" + region + "_matrix.txt";
        vectorPath = rootPath + "\\Output\\" + region + "_vector.txt";
        groupPath = rootPath + "\\Output\\" + region + "_group.txt";
        return "Switch to " + region + ".txt successful!\n";
    }

//===========================READ-FILE-FUNCTION=================================
    public String readRawData(Core_ProcessData pt) {
        FileReader dataFile;
        BufferedReader bufferReader;
        String readString;
        //==========================Check file exist============================
        try {
            dataFile = new FileReader(rawDataPath);
        } catch (FileNotFoundException e) {
            return rawDataPath + " does not exist!\n";
        }
        //=============================Read file================================
        bufferReader = new BufferedReader(dataFile);
        try {
            while ((readString = bufferReader.readLine()) != null) {
                if (pt.detectKeyword(readString) || pt.detectType(readString)) {
                    try {
                        writeBufferData(readString);
                    } catch (Exception ex) {
                        return "Error when appending the data to buffer.txt\n" + ex + "\n";
                    }
                }
            }
            bufferReader.close();
            return "Write data to buffer.txt successful!\n";
        } catch (IOException ex) {
            return "An error has occur at writing buffer.txt: " + ex + "\n";
        }
    }

    public String readBufferData(Core_ProcessData pt) {
        FileReader dataFile;
        BufferedReader bufferReader;
        String readString;
        //==========================Check file exist============================
        try {
            dataFile = new FileReader(bufferDataPath);
        } catch (FileNotFoundException e) {
            return bufferDataPath + " does not exist!\n";
        }
        //=============================Read file================================
        bufferReader = new BufferedReader(dataFile);
        try {
            String newWrite = "", writtenString = "";
            while ((readString = bufferReader.readLine()) != null) {
                if (readString.compareTo("matrix") == 0) {
                    if (newWrite.compareTo(writtenString) != 0) {
                        try {
                            writeMatrixData(newWrite);
                        } catch (Exception ex) {
                            return "Error when appending the data to the " + region + "_matrix.txt)\n" + ex + "\n";
                        }
                        writtenString = newWrite;
                    }
                } else if (readString.compareTo("vector") == 0) {
                    if (newWrite.compareTo(writtenString) != 0) {
                        try {
                            writeVectorData(newWrite);
                        } catch (Exception ex) {
                            return "Error when appending the data to the " + region + "_vector.txt)\n" + ex + "\n";
                        }
                        writtenString = newWrite;
                    }
                } else if (readString.compareTo("group") == 0) {
                    if (newWrite.compareTo(writtenString) != 0) {
                        try {
                            writeGroupData(newWrite);
                        } catch (Exception ex) {
                            return "Error when appending the data to the " + region + "_group.txt)\n" + ex + "\n";
                        }
                        writtenString = newWrite;
                    }
                }
                newWrite = readString;
            }
            bufferReader.close();
            return "Data processing successful!\n";
        } catch (IOException ex) {
            return "An error has occur at write data output: " + ex + "\n";
        }
    }

    public void writeBufferData(String dataToAppend) throws Exception{
        try (FileWriter fileWriter = new FileWriter(bufferDataPath, true);
                BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {
            bufferedWriter.write(dataToAppend);
            bufferedWriter.newLine();
        }
    }

    public void writeMatrixData(String dataToAppend) throws Exception{
        try (FileWriter fileWriter = new FileWriter(matrixPath, true);
                BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {
            bufferedWriter.write(dataToAppend);
            bufferedWriter.newLine();
        }
    }

    public void writeVectorData(String dataToAppend) throws Exception{
        try (FileWriter fileWriter = new FileWriter(vectorPath, true);
                BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {
            bufferedWriter.write(dataToAppend);
            bufferedWriter.newLine();
        }
    }
    
    public void writeGroupData(String dataToAppend) throws Exception{
        try (FileWriter fileWriter = new FileWriter(groupPath, true);
                BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {
            bufferedWriter.write(dataToAppend);
            bufferedWriter.newLine();
        }
    }

    public String clearBufferData() {
        try (FileWriter fileWriter = new FileWriter(bufferDataPath)) {
            fileWriter.write("");
            return  "Clear buffer.txt successful!\n";
        } catch (IOException e) {
            return "An error occurred while clearing the file." + e + "\n";
        }
    }

    public String clearMatrixData() {
        try (FileWriter fileWriter = new FileWriter(matrixPath)) {
            fileWriter.write("");
            return "Clear " + region + "_matrix.txt successful!\n";
        } catch (IOException e) {
            return "An error occurred while clearing the file." + e + "\n";
        }
    }

    public String clearVectorData() {
        try (FileWriter fileWriter = new FileWriter(vectorPath)) {
            fileWriter.write("");
            return "Clear " + region + "_vector.txt successful!\n";
        } catch (IOException e) {
            return "An error occurred while clearing the file." + e + "\n";
        }
    }
    
    public String clearGroupData() {
        try (FileWriter fileWriter = new FileWriter(groupPath)) {
            fileWriter.write("");
            return "Clear " + region + "_group.txt successful!\n";
        } catch (IOException e) {
            return "An error occurred while clearing the file." + e + "\n";
        }
    }
    
    public static boolean checkFileExistence(String path) {
        File file = new File(path);
        if (file.exists() && file.isFile()) {
            return true;
        } else {
            try {
                file.createNewFile();
                return false;
            } catch (IOException e) {
                return false;
            }
        }
    }
    
    public String openInWindows(String path) {
        try {
            File opener = new File(path);
            String typeOfOpener = "";
            if (opener.exists()) {
                if (opener.isFile()) typeOfOpener = "file";
                if (opener.isDirectory()) typeOfOpener = "folder";
                if (Desktop.isDesktopSupported()) {
                    Desktop.getDesktop().open(opener);
                    return "Open " + typeOfOpener + " successful!\n";
                } else {
                    return "Desktop is not supported on this platform\n";
                }
            } else {
                return "File does not exist or is not a valid file.\n";
            }
        } catch (IOException e) {
            return  "Error opening the file: \n" + e.getMessage() + "\n";
        }
    }
    
    public String showInfomation(){
        String result = "";
        result += "OWNER: DuyDuc94\n";
        result += "KEYWORD: " + Core_ProcessData.getKeywords();
        result += "TYPE: " + Core_ProcessData.getTypes();
        result += "ROOT PATH: " + rootPath + "\n";
        result += "OUTPUT PATH: " + outputPath + "\n";
        result += "DATA PATH: " + rawDataPath + "\n";
        result += "BUFFER PATH: " + bufferDataPath + "\n";
        result += "VECTOR PATH: " + vectorPath + "\n";
        result += "MATRIX PATH: " + matrixPath + "\n";
        result += "GROUP PATH: " + groupPath + "\n";
        return result;
    }
}
