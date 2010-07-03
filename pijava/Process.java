public abstract class Process implements Runnable {
    Env startEnv;

    public Process() {
	this.startEnv = new Env();
    }

    public Process(Env env) {
	this.startEnv = new Env(env);
    }

    public Env newChannel(Env env, String name) {
	Channel channel = new Channel();
	Env res = new Env(env);
	res.addBind(name, channel);
	return res;
    }

    public Env send(Env env, String name1, String name2) {
	env.getBindChannel(name1).send(env.getBind(name2));
	return env;
    }

    public Env receive(Env env, String name1, String name2)  {
	Object received = env.getBindChannel(name1).receive();
	Env res = new Env(env);
	res.addBind(name2, received);
	return res;
    }
    public Env receive(Env env, String name1, String[] names)  {
	Object[] received = (Object[])env.getBindChannel(name1).receive();
	Env res = new Env(env);
	for (int i=0; i<received.length; i++)
	    res.addBind(names[i], received[i]);
	return res;
    }

    public void bangReceive(Env env, String name1, String name2, Process p)  {
	while (true) {
	    Object channel = env.getBindChannel(name1).receive();
	    p.startEnv = new Env(env);
	    p.startEnv.addBind(name2, channel);
	    new Thread(p).start();
	}
    }
    public void bangReceive(Env env, String name1, String[] names, Process p)  {
	while (true) {
	    Object [] received = (Object [])env.getBindChannel(name1).receive();
	    p.startEnv = new Env(env);
	    for (int i=0; i<received.length; i++)
		p.startEnv.addBind(names[i], received[i]);
	    new Thread(p).start();
	}
    }

    public void par(Env env, Process p1, Process p2) {
	p1.startEnv = new Env(env);
	p2.startEnv = new Env(env);
	new Thread(p1).start();
	new Thread(p2).start();
    }

    public void run() {
	this.execute(this.startEnv);
    }
    abstract public void execute(Env env);
}