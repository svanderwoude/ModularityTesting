import java.io.File;
import java.io.FileNotFoundException;
import java.lang.*;
import java.util.*;
import java.util.regex.Pattern;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseProblemException;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;


public class MyModularity{
    public static void main(String[] args){
        String paths[] = {
                "dropwizard",
                "iot-2",
                "iot-3",
                "iot-starterkit",
                "light-rest-4j",
                "mirror",
                "ninja",
                "spark",
        };

        for(String path : paths) {
            File root = new File("/home/svanderwoude/UvA/Thesis/Projects/java/"+path+"/");
            List<File> files = getFiles(root);
            List<Integer> volumes = getVolume(files);
            int totalvolume = volumes.stream().mapToInt(Integer::intValue).sum();
            int small = 0, medium = 0, large = 0, very_large = 0;
            int unit_score = 0;
            float total = (float) volumes.size();

            for(Integer vol : volumes){
                if(vol <= 15){
                    small++;
                }
                if(vol > 15){
                    medium++;
                }
                if(vol > 30){
                    large++;
                }
                if(vol > 60){
                    very_large++;
                }
            }

            if(small / total >= 0.573 && medium / total < 0.437 && large / total <= 0.223 && very_large / total <= 0.069){
                unit_score = 5;
            }else if(small / total >= 0.50 && medium / total <= 0.50 && large / total <= 0.25 && very_large / total <= 0.10){
                unit_score = 4;
            }else if(small / total >= 0.45 && medium / total <= 0.55 && large / total <= 0.30 && very_large / total <= 0.125){
                unit_score = 3;
            }else if(small / total >= 0.40 && medium / total <= 0.60 && large / total <= 0.35 && very_large / total <= 0.15){
                unit_score = 2;
            }else{
                unit_score = 1;
            }

            if(files.size() > 0){
                double modularity = calculateModularity(files);
                System.out.println(path + ": " + modularity + " " + totalvolume + " " + unit_score);
            }else{
                System.out.println(path + ": DISCARDED");
            }
        }
    }

    private static String fileExtension(File file){
        String name = file.getName();
        int i = name.lastIndexOf(".");
        String ext = i > 0 ? name.substring(i + 1) : "";
        return ext;
    }

    private static List<File> getFiles(File root){
        List<File> files = new ArrayList<>();
        int errorcount = 0;

        try {
            for (File file : root.listFiles()) {
                if (file.isDirectory()) {
                    files.addAll(getFiles(file));
                } else if (fileExtension(file).equals("java") &&
                        !file.getAbsolutePath().contains("test")) {
                    try {
                        CompilationUnit cu = JavaParser.parse(file);
                        Scanner sc = new Scanner(file);

                        if (sc.hasNextLine()) {
                            files.add(file);
                        }
                    } catch (FileNotFoundException e) {

                    } catch (ParseProblemException e) {
                        errorcount += 1;
                    }
                }
            }
        }catch(NullPointerException e){ }

        if(files.size() == 0 || (float) errorcount / files.size() > 0.30){
            return new ArrayList<>();
        }

        return files;
    }

    private static List<Integer> getVolume(List<File> files){
        List<Integer> counts = new ArrayList<>();

        for(File file : files){
            try {
                Scanner sc = new Scanner(file);
                int linecount = 0;

                while (sc.hasNextLine()) {
                    String line = sc.nextLine();

                    line = line.trim();
                    if (!"".equals(line) && !line.startsWith("//")) {
                        linecount++;
                    }
                }

                counts.add(linecount);
            }catch(FileNotFoundException e){ }
        }

        return counts;
    }

    private static double calculateModularity(List<File> files){
        List<Float> allPerc = new ArrayList<>();

        for(File file : files){
            try{
                String prefix = file.getName() + "_";
                List<String> single_imports = new ArrayList<>();
                List<String> prefixed_calls = new ArrayList<>();
                List<String> prefixed_declarations = new ArrayList<>();
                CompilationUnit cu = JavaParser.parse(file);

                // Imports
                ImportVisitor iv = new ImportVisitor();
                iv.visit(cu, null);

                for(String i : iv.imports){
                    if(i.startsWith("java")){
                        String[] parts = i.split(Pattern.quote("."));
                        single_imports.add(parts[parts.length - 1]);
                    }
                }

                // Method calls
                CallVisitor cv = new CallVisitor();
                cv.visit(cu, null);

                for(String call : cv.calls){
                    if(!single_imports.contains(call)) {
                        prefixed_calls.add(prefix + call);
                    }
                }

                // Method declarations
                MethodVisitor mv = new MethodVisitor();
                mv.visit(cu, null);

                for(String decl : mv.methods){
                    prefixed_declarations.add(prefix + decl);
                }

                // Modularity calculation
                int internal = 0;
                int external = 0;

                for(String call : prefixed_calls){
                    if(prefixed_declarations.contains(call)){
                        internal += 1;
                    }else{
                        external += 1;
                    }
                }

                float perc = 1.0f;

                if(internal + external > 0){
                    perc = internal / (internal + external);
                }

                allPerc.add(perc);
            }catch(FileNotFoundException | ParseProblemException e){ }
        }

        return allPerc.stream().mapToDouble(val -> val).average().orElse(1.0);
    }

    private static class ImportVisitor extends VoidVisitorAdapter<Void> {
        public List<String> imports = new ArrayList<>();

        @Override
        public void visit(ImportDeclaration n, Void arg) {
            String name = n.getName().toString();
            this.imports.add(name);
            super.visit(n, arg);
        }
    }

    private static class MethodVisitor extends VoidVisitorAdapter<Void> {
        public List<String> methods = new ArrayList<>();

        @Override
        public void visit(MethodDeclaration n, Void arg) {
            String name = n.getName().toString();
            this.methods.add(name);
            super.visit(n, arg);
        }
    }

    private static class CallVisitor extends VoidVisitorAdapter<Void> {
        public List<String> calls = new ArrayList<>();

        @Override
        public void visit(MethodCallExpr n, Void arg) {
            String name = n.getName().toString();
            this.calls.add(name);
            super.visit(n, arg);
        }
    }
}
