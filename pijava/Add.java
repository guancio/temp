public class Add extends Process {

    class Service extends Process {
	public void execute(Env env) {
	    this.bangReceive(env, "add", new String[]{"x", "y", "r"}, new AddProcess());
	}
    }
    class AddProcess extends Process {
	public void execute(Env env) {
	    int x = (Integer)env.getBind("x");
	    int y = (Integer)env.getBind("y");
	    env.getBindChannel("r").send(x+y);
	}
    }

    class Client extends Process {
	public void execute(Env env) {
	    env = this.newChannel(env, "resp");
	    this.par(env, new ClientSend(), new ClientRecv());
	}
    }

    class ClientSend extends Process {
	public void execute(Env env) {
	    env.getBindChannel("add").send(new Object[]{1,2,env.getBind("resp")});
	}
    }
    class ClientRecv extends Process {
	public void execute(Env env) {
	    env = this.receive(env, "resp", "v");
	    new Print().execute(env);
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
	env = this.newChannel(env, "add");
	this.par(env, new Service(), new Client());
    }

    public static void main(String[] args) {
	Add add = new Add();
	new Thread(add).start();
    }
}