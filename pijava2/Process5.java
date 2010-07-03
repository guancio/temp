
    public class Process5 extends Process {
       public void execute(Env env) {
          


          env.getBindChannel("add").send(new Object[] {1,2,env.getBind("resp")});
    
       }
       public static void main(String[] args) {
           Process5 process = new Process5();
           new Thread(process).start();
       }
    }
    