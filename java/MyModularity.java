import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.*;
import java.util.*;


public class MyModularity{
    public static void main(String[] args){
        File root = new File(".");
        calculateModularity(getFiles(root));
    }

    public static String fileExtension(File file){
        String name = file.getName();
        int i = name.lastIndexOf(".");
        String ext = i > 0 ? name.substring(i + 1) : "";
        return ext;
    }

    public static List<File> getFiles(File root){
        List<File> files = new ArrayList<>();

        for(File file : root.listFiles()){
            if(file.isDirectory()){
                files.addAll(getFiles(file));
            }else if(fileExtension(file).equals("java") &&
                     !file.getAbsolutePath().contains("test")){
                try{
                    Scanner sc = new Scanner(file);

                    if(sc.hasNextLine()){
                        files.add(file);
                    }
                    
                }catch(FileNotFoundException e){ }
            }
        }

        return files;
    }

    public static float calculateModularity(List<File> files){
        try{
            Scanner sc = new Scanner(files.get(0));

            while(sc.hasNextLine()){
                String str = sc.nextLine();
            }
        }catch(FileNotFoundException e){ }
        return 1.0f;
    }
}
