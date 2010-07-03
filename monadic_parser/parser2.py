# Parser a: String -> [(a, String)] dove a e' un Tree

def concat(l):
    return reduce(
        lambda li,lr: li+lr, l,[]
        )

def concat_maps(maps):
    res = {}
    for m in maps:
        for x in m:
            res[x] = m[x]
    return res

result = lambda v: \
         lambda inp: \
         [(v, inp)]

zero = lambda inp: []

item = lambda inp: \
       [] if inp == [] or inp == "" else \
       [(inp[0], inp[1:])]

bind = lambda p: \
       lambda f:\
       lambda inp:\
       concat([f(v)(inp1) for (v,inp1) in p(inp)])

attribute = bind(item)(lambda (event, name, value):\
        result({name:value}) if event =="attr" else
        zero
      )

plus = lambda p:\
       lambda q:\
       lambda inp:\
       q(inp) if q(inp) != [] else\
       p(inp)

attr_list = plus(result({}))(
    bind(attribute)(lambda att:\
    bind(attr_list)(lambda ats:\
        result(concat_maps([att, ats]))
    )))

start_elem = bind(item)(lambda (event, name, value):\
        result(name) if event=="element" else \
        zero)

end_elem = lambda tag:\
           bind(item)(lambda (event, name, value):\
            result(name) if event=="end_element" and \
                      name == tag else \
            zero)

elem = bind(start_elem)  (lambda e:\
       bind(attr_list)   (lambda attrs:\
       bind(elem_list)   (lambda es:\
       bind(end_elem(e)) (lambda end:\
            result([e, attrs] + es)
        ))))

elem_list = plus(result([]))(
    bind(elem)(lambda e:\
    bind(elem_list)(lambda es:\
        result([e] + es)
    )))

stream = [
    ("attr", "name", "a"),
    ("attr", "surname", "b"),
    ("element", "person", ""),
    ("attr", "name", "c"),
    ("attr", "surname", "d")
    ]
stream1 = [
    ("element", "person", ""),
    ("attr", "name", "a"),
    ("attr", "surname", "b"),
    ("end_element", "person", ""),
    ("element", "person", ""),
    ("attr", "name", "c"),
    ("attr", "surname", "d"),
    ("end_element", "person", "")
    ]
stream = [
    ("element", "person", ""),
    ("attr", "name", "a"),
    ("attr", "surname", "b"),
      ("element", "child", ""),
      ("attr", "age", "10"),
      ("end_element", "child", ""),
      ("element", "child", ""),
      ("attr", "age", "20"),
      ("end_element", "child", ""),
      ("element", "child", ""),
      ("end_element", "child", ""),
    ("end_element", "person", ""),
    ("element", "person", ""),
    ("attr", "name", "c"),
    ("attr", "surname", "d"),
    ("end_element", "person", "")
    ]
# print attribute(stream)
# print attribute(stream1)
# print attr_list(stream)
# print start_elem(stream1)
# print repr(elem_list(stream1)[0])

#print elem_list(stream)
