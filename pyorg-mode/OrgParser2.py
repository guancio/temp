txt = open("/home/guancio/Desktop/todo.org").read()
lines = txt.split("\n")

class OrgNode(object):
    TEXT, OUTLINE, LIST = range(3)
    def __init__(self, node_type=TEXT, title="", parent=None, depth=0):
        self.title = title
        self.childs = []
        self.parent = parent
        self.node_type = node_type
        self.depth = depth
    def __str__(self, ):
        return """
title: %s
depth: %d
childs: %s
        """ % (self.title, self.depth, str(self.childs))



doc_node = OrgNode(OrgNode.OUTLINE)
curr_node = doc_node
for line in lines:
    if line[:1] == "*":
        depth = line.find(" ")
        while curr_node.node_type != OrgNode.OUTLINE:
            curr_node = curr_node.parent
        while curr_node.depth >= depth:
            curr_node = curr_node.parent

        next_node = OrgNode(OrgNode.OUTLINE, line[depth:], curr_node, depth)
        curr_node.childs.append(next_node)
        curr_node = next_node

    elif line.lstrip()[:2] == "+ ":
        depth = line.find("+")
        while curr_node.node_type == OrgNode.LIST and curr_node.depth > depth:
            curr_node = curr_node.parent

        if curr_node.node_type != OrgNode.LIST or curr_node.depth < depth:
            next_node = OrgNode(OrgNode.LIST, "", curr_node, depth)
            curr_node.childs.append(next_node)
            curr_node = next_node

        curr_node.childs.append(line[depth:])
    else:
        curr_node.childs.append(line)
