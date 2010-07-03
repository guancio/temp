public class Main extends Process {

    class Process1 extends Process {
	public void execute(Env env) {
	    env = this.send(env, "x", "y");
	}
    }
    class Process2 extends Process {
	public void execute(Env env) {
	    env = this.receive(env, "x", "z");
	    System.out.println(env.getBind("x"));
	    System.out.println(env.getBind("y"));
	    System.out.println(env.getBind("z"));
	}
    }
    class Process3 extends Process {
	public void execute(Env env) {
	    this.bangReceive(env, "x", "z", new Print());
	}
    }
    class Print extends Process {
	public void execute(Env env) {
	    for (String name: env.getNames()) {
		System.out.println(name + ":" + env.getBind(name));
	    }
	}
    }

    public void execute(Env env) {
	env = p1(env);
	env = p2(env);
	
	//this.par(env, new Process1(), new Process2());
	this.par(env, new Process1(), new Process3());

    }

    public Env p1(Env env) {
	return this.newChannel(env, "x");
    }
    public Env p2(Env env) {
	return this.newChannel(env, "y");
    }
    
    public static void main(String[] args) {
	Main main = new Main();
	new Thread(main).start();
    }
}