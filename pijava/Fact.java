public class Fact extends Process {

    class Service extends Process {
	public void execute(Env env) {
	    this.bangReceive(env, "fact", new String[]{"y", "res"}, new FactProcess());
	}
    }
    class FactProcess extends Process {
	public void execute(Env env) {
	    long y = (Long)env.getBind("y");
	    if (y == 0) {
		env.getBindChannel("res").send(0L);
		return;
	    }
	    if (y == 1) {
		env.getBindChannel("res").send(1L);
		return;
	    }
	    env = this.newChannel(env, "res1");
	    this.par(env, new P1(), new P2());
	}
    }
    class P1 extends Process {
	public void execute(Env env) {
	    long y = (Long)env.getBind("y");
	    env.getBindChannel("fact").send(new Object[]{y-1, env.getBind("res1")});
	}
    }
    class P2 extends Process {
	public void execute(Env env) {
	    env = this.receive(env, "res1", "v");
	    long y = (Long)env.getBind("y");
	    long v = (Long)env.getBind("v");
	    env.getBindChannel("res").send(y*v);
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
	    env.getBindChannel("fact").send(new Object[]{20L,env.getBind("resp")});
	}
    }
    class ClientRecv extends Process {
	public void execute(Env env) {
	    env = this.receive(env, "resp", "v");
	    new Print().execute(env);
	    Process p = new Client();
	    p.startEnv = new Env(env);
	    new Thread(p).start();
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
	env = this.newChannel(env, "fact");
	this.par(env, new Service(), new Client());
    }

    public static void main(String[] args) {
	Fact fact = new Fact();
	new Thread(fact).start();
    }
}