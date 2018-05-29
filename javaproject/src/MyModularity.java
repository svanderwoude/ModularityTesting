import java.io.File;
import java.io.FileNotFoundException;
import java.lang.*;
import java.util.*;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;


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
        for(File file : files){
            try{
                CompilationUnit cu = JavaParser.parse(file);
//                cu.accept(new MethodVisitor(), null);
                cu.accept(new CallVisitor(), null);
            }catch(FileNotFoundException e){
                System.out.println("error");
            }
        }

        return 1.0f;
    }

    private static class MethodVisitor extends VoidVisitorAdapter<Void> {
        @Override
        public void visit(MethodDeclaration n, Void arg) {
            /* here you can access the attributes of the method.
             this method will be called for all methods in this
             CompilationUnit, including inner class methods */
            System.out.println(n.getName());
            super.visit(n, arg);
        }
    }

    private static class CallVisitor extends VoidVisitorAdapter<Void> {
        @Override
        public void visit(MethodCallExpr n, Void arg) {
            /* here you can access the attributes of the method.
             this method will be called for all methods in this
             CompilationUnit, including inner class methods */
            System.out.println(n.getName());
            super.visit(n, arg);
        }
    }
}
