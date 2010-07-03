from lxml import etree
from lxml import objectify

counter = 0

def compile_new(process):
    (child_body, deps) = compile_process(process.getchildren()[0])
    body = """
              env = this.newChannel(env, \"%s\");
              %s
         """ % (process.get("channel"), child_body)
    return (body, deps)

def compile_par(process):
    child0 = enclose_process(process.getchildren()[0])
    child1 = enclose_process(process.getchildren()[1])
    (ID0, code0) = child0[0]
    (ID1, code1) = child1[0]
    body = """
              this.par(env, new Process%d(), new Process%d());
         """ % (ID0, ID1)
    return (body, child0 + child1)

def compile_bang_receive(process):
    deps = enclose_process(process.getchildren()[0])
    ID, child = deps[0]
    channel_code = '"%s"' % process.get("channel")
    binders = process.get("binders").split(",")
    binders_code = "new String[] {" +\
                   ",".join(['"' + var + '"' for var in binders]) + \
                   "}"
    body = """
              this.bangReceive(env, %s, %s, new Process%d());
         """ % (channel_code, binders_code, ID)
    return (body, deps)

def compile_receive(process):
    (child_body, deps) = compile_process(process.getchildren()[0])
    channel_code = '"%s"' % process.get("channel")
    binders = process.get("binders").split(",")
    binders_code = "new String[] {" +\
                   ",".join(['"' + var + '"' for var in binders]) + \
                   "}"
    body = """
              env = this.receive(env, %s, %s);
         """ % (channel_code, binders_code)
    body += child_body
    return (body, deps)

def compile_value_int(value):
    if value[0] == "+":
        params = value[2:].split(" ")
        value0, code0 = compile_value_int(params[0])
        value1, code1 = compile_value_int(params[1])
        return (value0 + "+" + value1, code0 + "\n" + code1)
    try:
        int(value)
        return (value, "")
    except:
        pass
    
    return ("%s" % value, 'int %s = (Integer) env.getBind("%s");' % (value, value))

def compile_value(value):
    if value[0] == "+":
        return compile_value_int(value)
    try:
        int(value)
        return compile_value_int(value)
    except:
        pass
    
    return ('env.getBind("%s")' % value, "")

def compile_send(process):
    values = process.get("value").split(",")
    codes = []
    exp = []
    for value in values:
        (res, code) = compile_value(value)
        codes.append(code)
        exp.append(res)

    res = "\n".join(codes)
    res += """
          env.getBindChannel(\"%s\").send(new Object[] {%s});
    """%(process.get("channel"), ",".join(exp))

    return (res, [])

def compile_x_print(process):
    values = process.get("value").split(",")
    codes = []
    exp = []
    for value in values:
        (res, code) = compile_value(value)
        codes.append(code)
        exp.append(res)

    res = "\n".join(codes)
    for e in exp:
        res += """
        System.out.println(%s);
        """%(e)

    return (res, [])

def compile_process(process):
    if process.tag == "new":
        return compile_new(process)
    if process.tag == "par":
        return compile_par(process)
    if process.tag == "bangReceive":
        return compile_bang_receive(process)
    if process.tag == "send":
        return compile_send(process)
    if process.tag == "receive":
        return compile_receive(process)
    if process.tag == "x_print":
        return compile_x_print(process)
    return (process.tag, [])

def enclose_process(process):
    global counter
    counter += 1
    my_id = counter
    (body, deps) = compile_process(process)
    
    build = """
    public class Process%d extends Process {
       public void execute(Env env) {
          %s
       }
       public static void main(String[] args) {
           Process%d process = new Process%d();
           new Thread(process).start();
       }
    }
    """%(my_id, body, my_id, my_id)
    return [(my_id, build)] + deps
    

source = open("fact.pi.xml").read()
root = objectify.fromstring(source)


res = enclose_process(root)
for s in res:
    open("Process%d.java"%s[0], "w").write(s[1])
