
    public class Process6 extends Process {
       public void execute(Env env) {
          
              env = this.receive(env, "resp", new String[] {"v"});
         
        System.out.println(env.getBind("v"));
        
       }
       public static void main(String[] args) {
           Process6 process = new Process6();
           new Thread(process).start();
       }
    }
    