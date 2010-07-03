public class Test {
    public void test() {
	Object elem = new Integer(1);
	try {
	    elem.wait();
	    System.out.println("ciao");
	}
	catch (Exception ex) {
	    System.out.println("exception");
	}
    }
}