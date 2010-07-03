import java.util.List;
import java.util.ArrayList;

public class Channel {
    static int chCounter = 0;
    int channelId;
    List<Object> message = null;

    public Channel() {
	synchronized (Channel.class) {
	    chCounter++;
	    this.channelId = chCounter;
	}
	this.message = new ArrayList<Object>();
    }
    
    public int getChannelId() {
	return channelId;
    }

    public Object receive() {
	synchronized (this) {
	    while (this.message.size() == 0) {
		try {
		    this.wait();
		}
		catch (InterruptedException ex) {
		    return null;
		}
	    }
	    Object res = this.message.get(0);
	    this.message.remove(0);
	    return res;
	}
    }

    public void send(Object message) {
	synchronized (this) {
	    this.message.add(message);
	    this.notifyAll();
	}
    }
}