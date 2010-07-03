# Parser a: String -> [(a, String)] dove a e' un Tree

def result(v):
    """ Success without consuming the input
    result: a -> Parser a
    """
    return lambda inp: [(v, inp)]

zero = lambda inp: []
"""
Always fails
zero: Parser a
"""

item = lambda inp: [] \
       if inp == [] or inp == ""\
       else [(inp[0], inp[1:])]
"""Successful consume a char
item: Parser Char
"""

def bind(p):
    """bind parsing
    
    Arguments:
    - `p`: Parser a
    """
    return lambda f:\
           lambda inp:\
           reduce(lambda l,lr: l+lr, \
                  [f(v)(inp1) for (v,inp1) in p(inp)],\
                  [])

seq = lambda p:\
      lambda q:\
      bind(p)(lambda x:\
      bind(q)(lambda y:\
              result(x+y)
      ))

sat = lambda p:\
      bind(item)(lambda x:\
      result(x) if p(x) else zero
      )

is_char = lambda x:\
        sat(lambda y:x==y)

is_number = sat(lambda y:'0'<=y and y<='9')
letter = sat(lambda y:'a'<=y and y<='z')

plus = lambda p:\
       lambda q:\
       lambda inp:\
       p(inp) + q(inp)


word = plus(result(""))(
    bind(letter)(lambda x:\
    bind(word)(lambda xs:\
        result(x+xs)
    )))

print result("c")("ciao")

print zero("ciao")

print item("ciao")

print bind(item)(
    lambda x:\
    result(x)
    )("ciao")

r=bind(item)(lambda x:\
  bind(item)(lambda y:\
  bind(item)(lambda z:\
             result((x,z,y))
  )))

print r("ciao")
print seq(item)(item)("ciao")
print seq(is_char("x"))(item)("ciao")
print seq(is_char("c"))(item)("ciao")
print seq(is_number)(is_char("i"))("ciao")
print seq(is_number)(is_char("i"))("1iao")
print seq(is_number)(is_char("c"))("1iao")

c_or_num = plus(is_number)(is_char("c"))
c_or_c = plus(is_char("c"))(is_char("c"))
print c_or_num("1iao")
print c_or_c("ciao")

print word("guancio primo")
print word("guancio")


attr = bind(item)(lambda (event, name, value):\
        result("%s=%s" % (name, value)) if event =="attr" else
        zero
      )
# elem = bind(item)(lambda (event, name, value):\
#         result("%s=%s" % (name, value)) if event =="attr" else
#         zero
#       )

# stream = [
#     ("attr", "name", "a"),
#     ("attr", "name", "b"),
#     ("element", "person", ""),
#     ("attr", "name", "c"),
#     ("attr", "name", "d")
#     ]
# stream1 = [
#     ("element", "person", ""),
#     ("attr", "name", "a"),
#     ("attr", "name", "b"),
#     ("element", "person", ""),
#     ("attr", "name", "c"),
#     ("attr", "name", "d")
#     ]
# print seq(attr)(attr)(stream)
# print seq(seq(attr)(attr))(attr)(stream)
