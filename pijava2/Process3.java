
    public class Process3 extends Process {
       public void execute(Env env) {
          int x = (Integer) env.getBind("x");
int y = (Integer) env.getBind("y");
          env.getBindChannel("r").send(new Object[] {x+y});
    
       }
       public static void main(String[] args) {
           Process3 process = new Process3();
           new Thread(process).start();
       }
    }
    