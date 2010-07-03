
    public class Process2 extends Process {
       public void execute(Env env) {
          
              this.bangReceive(env, "add", new String[] {"x","y","r"}, new Process3());
         
       }
       public static void main(String[] args) {
           Process2 process = new Process2();
           new Thread(process).start();
       }
    }
    