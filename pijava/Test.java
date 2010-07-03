public class Test {
    public static void main(String [] arg) {
	final String name = arg[0];
	class Guancio {
	    public void printName() {
		System.out.println(name);
	    }
	}
	new Guancio().printName();
    }
}