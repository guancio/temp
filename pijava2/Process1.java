
    public class Process1 extends Process {
       public void execute(Env env) {
          
              env = this.newChannel(env, "add");
              
              this.par(env, new Process2(), new Process4());
         
         
       }
       public static void main(String[] args) {
           Process1 process = new Process1();
           new Thread(process).start();
       }
    }
    