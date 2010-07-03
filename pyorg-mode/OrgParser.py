from pyparsing import *


txt = open("/home/guancio/Desktop/todo.org").read()

class OrgHeadline(object):
    """
    """
    
    def __init__(self, depth, title, text, childs=[]):
        """
        
        Arguments:
        - `depth`:
        - `title`:
        - `text`:
        - `childs`:
        """
        self._depth = depth
        self._title = title
        self._text = text
        self._childs = childs

    @staticmethod
    def extend_childs(headline, childs):
        """
        """
        headline._childs += childs
        return headline

    def __str__(self, ):
        """
        """
        return """depth: %s
title:%s
text:%s
childs:%s""" % (self._depth, self._title, self._text, str(self._childs))


def printDebug(t):
    print t
    return t

def outline(depth):
    if depth > 10:
        return Empty()
    res = Forward()
    child = outline(depth+1)
    res << \
        Group(
        (
            "*" * depth + " " + \
            ZeroOrMore(CharsNotIn("\n")) + \
            LineEnd() + \
            ZeroOrMore(CharsNotIn("*")) \
        ).setParseAction(lambda s,l,t: OrgHeadline(depth,t[1],t[3] if len(t) >=4 else "")) + \
        ZeroOrMore(child)
        ).setParseAction(lambda s,l,t: OrgHeadline.extend_childs(t[0][0], t[0][1:] if len(t[0]) > 1 else []))
    return res

r = ZeroOrMore(outline(1)).parseString(txt[24:])

