# Parser a: String -> [(a, String)] dove a e' un Tree

def concat(l):
    return reduce(
        lambda li,lr: li+lr, l,[]
        )

# concat_maps: [{a}] -> [{a}]
def concat_maps(maps):
    res = {}
    for m in maps:
        for x in m:
            res[x] = m[x]
    return res

# result: a -> b -> [(a,b)]
result = lambda v: \
         lambda inp: \
         [(v, inp)]

# zero: a -> []
zero = lambda inp: []

# item: [a]->[(a, [a])]
item = lambda inp: \
       [] if inp == [] else \
       [(inp[0], inp[1:])]

# bind: (a->[(b,c)]) -> (b->(c->[d])) -> a -> [d]
bind = lambda p: \
       lambda f:\
       lambda inp:\
       concat([f(v)(inp1) for (v,inp1) in p(inp)])

# attribute:
# bind: (a->[(b,c)]) -> (b->(c->[d])) -> a -> [d]
# item: [a']->[(a', [a'])]
# bind(item) : a' = [a]; b = a'; c = [a'] =>
# bind(item) : (a->([a]->[d'])) -> [a] -> [d'] =>
# bind(item) : (a->([a]->[b])) -> [a] -> [b]
# result: a -> b -> [(a,b)]
# result({name:value}): a' ={str:str} =>
# result({name:value}): b' ->[({str:str}, b')] =>
# result({name:value}): a ->[({str:str}, a)]
# zero: a-> []
# lambda: (str, str, str) -> a ->[({str:str}, a)]
# bind(item)(lambda): a' = (str, str, str); a=[a']=[(str, str, str)]; b'=({str:str}, a)
# bind(item)(lambda): [(str, str, str)] -> [({str:str}, [(str, str, str)])]
attribute = bind(item)(lambda (event, name, value):\
        result({name:value}) if event =="attr" else
        zero
      )

# plus:
# q: a -> [b]
# p: a -> [b]
# plus: (a->[b]) -> (a-> [b]) -> (a -> [b])
plus = lambda p:\
       lambda q:\
       lambda inp:\
       q(inp) + p(inp)
       #q(inp) if q(inp) != [] else\
       #p(inp)

# attr_list
# plus: (a->[b]) -> (a-> [b]) -> (a -> [b])
# result: a -> b -> [(a,b)]
# result({}): a' = {} => b' -> [({}, b')]
# result({}): a -> [({}, a)]
# plus(result({})): a'=a; b'=({}, a) =>
# plus(result({})): (a-> [({}, a)]) -> (a -> [({}, a)])
# concat_maps: [{a}] -> [{a}]
# concat_maps([att, ats]): att={a}, ats={a} => [{a}]
# result(concat_maps([att, ats])): a'= [{a}] =>
# result(concat_maps([att, ats])): b -> [([{a}],b)]
# lambda ats: {a} -> b -> [([{a}],b)]
# bind: (a->[(b,c)]) -> (b->(c->[d])) -> a -> [d]
# bind(attr_list): X = (a->[(b,c)])
# bind(attr_list)(lambda ats): b'={a}; c'=b; d'=([{a}],b) =>
# bind(attr_list)(lambda ats): a' -> [([{a}],b)] and X = (a'->[({a},b)]) =>
# bind(attr_list)(lambda ats): a -> [([{b}],c)] and X = (a->[({b},c)])
# lambda att: {b} -> a -> [([{b}],c)] and X = (a->[({b},c)]
# bind(attribute):
# attribute: [(str, str, str)] -> [({str:str}, [(str, str, str)])]
# bind(attribute): a' = [(str, str, str)]; b'={str:str}; c'=[(str, str, str)]
# bind(attribute): ({str:str}->([(str, str, str)]->[a])) -> [(str, str, str)] -> [a]
# bind(attribute)(lambda att): b=str:str; a=([(str, str, str)]->[a']))
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
