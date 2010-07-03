import java.util.Map;
import java.util.Set;
import java.util.HashMap;

public class Env {
    private Map<String, Object> env;

    public Env() {
	env = new HashMap<String, Object>();
    }

    public Env(Env src) {
	env = new HashMap<String, Object>();
	for (String name:src.getNames()) {
	    env.put(name, src.getBind(name));
	}
    }

    public Env(Env src, String[] names) {
	env = new HashMap<String, Object>();
	for (int i=0; i<names.length; i++) {
	    if (env.get(names[i]) != null)
		env.put(names[i], src.getBind(names[i]));
	}
    }

    public Object getBind(String name) {
	return env.get(name);
    }
    public Channel getBindChannel(String name) {
	return (Channel)env.get(name);
    }

    public Set<String> getNames() {
	return env.keySet();
    }
    
    public void addBind(String name, Object value) {
	env.put(name, value);
    }
}