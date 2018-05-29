import java.io.File;
import java.io.FileNotFoundException;
import java.lang.*;
import java.util.*;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseProblemException;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;


public class MyModularity{
    public static void main(String[] args){
        File root = new File("/home/svanderwoude/UvA/Thesis/Projects/java/dropwizard/");
        double modularity = calculateModularity(getFiles(root));
        System.out.println(modularity);
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

        for(File file : root.listFiles()){
            if(file.isDirectory()){
                files.addAll(getFiles(file));
            }else if(fileExtension(file).equals("java") &&
                    !file.getAbsolutePath().contains("test")){
                try{
                    CompilationUnit cu = JavaParser.parse(file);
                    Scanner sc = new Scanner(file);

                    if(sc.hasNextLine()){
                        files.add(file);
                    }

                }catch(FileNotFoundException e){

                }catch(ParseProblemException e){
                    errorcount += 1;
                }
            }
        }

        if((float) errorcount / files.size() > 0.30){
            return new ArrayList<>();
        }

        return files;
    }

    private static double calculateModularity(List<File> files){
        List<Float> allPerc = new ArrayList<>();

        for(File file : files){
            try{
                String prefix = file.getName() + "_";
                List<String> prefixed_calls = new ArrayList<>();
                List<String> prefixed_declarations = new ArrayList<>();
                CompilationUnit cu = JavaParser.parse(file);

                // Method calls
                CallVisitor cv = new CallVisitor();
                cv.visit(cu, null);

                for(String call : cv.calls){
                    prefixed_calls.add(prefix + call);
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
