
    public class Process4 extends Process {
       public void execute(Env env) {
          
              env = this.newChannel(env, "resp");
              
              this.par(env, new Process5(), new Process6());
         
         
       }
       public static void main(String[] args) {
           Process4 process = new Process4();
           new Thread(process).start();
       }
    }
    