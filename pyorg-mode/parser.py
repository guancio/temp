import re

txt = open("sc.org").read()

cursor_pos = 0

ORG_WORD, ORG_LINK, ORG_SEP, ORG_EMPTY_LINE, ORG_LIST = range(5)

def org_cursor_type():
    """
    """
    if re.match("\n[ ]*?\n", txt[cursor_pos:]) is not None:
        return ORG_EMPTY_LINE
    if re.match("\[\[.*\]\]", txt[cursor_pos:]) is not None:
        return ORG_LINK
    if re.match("\d+\.", txt[cursor_pos:]) is not None:
        return ORG_LIST
    if re.match("[ ,.:;\n]", txt[cursor_pos:]) is not None:
        return ORG_SEP
    return ORG_WORD

def org_parse_link():
    res = re.match("\[\[(.*?)\](?:\[(.*)\])?\]", txt[cursor_pos:])
    if res is None:
        return None
    res = res.groups()
    if res[1] is None:
        return (res[0], res[0])
    return res

def org_parse_word():
    res = re.match("(.*?)[ ,.:;\n]", txt[cursor_pos:])
    if res is None:
        return None
    return res.groups()[0]

def org_parse_sep():
    res = re.match("([ ,.:;\n])", txt[cursor_pos:])
    if res is None:
        return None
    return res.groups()[0]

def org_move_after_link():
    global cursor_pos
    res = re.search("\]\]", txt[cursor_pos:])
    cursor_pos += res.span()[1]
    return cursor_pos

def org_move_after_word():
    global cursor_pos
    try:
        res = re.search("[ ,.:;\n]", txt[cursor_pos:])
    except:
        cursor_pos = len(txt)
        return cursor_pos
    if res is None:
        cursor_pos = len(txt)
        return cursor_pos
    cursor_pos += res.span()[1]-1
    return cursor_pos

def org_move_after_list():
    global cursor_pos
    res = re.search("\d+\.[ ]", txt[cursor_pos:])
    if res is None:
        cursor_pos = len(txt)
        return cursor_pos
    cursor_pos += res.span()[1]
    return cursor_pos

def org_move_after_empty_line():
    global cursor_pos
    res = re.search("\n[ ]*?\n", txt[cursor_pos:])
    if res is None:
        cursor_pos = len(txt)
        return cursor_pos
    cursor_pos += res.span()[1]
    return cursor_pos

def org_move_after_sep():
    global cursor_pos
    cursor_pos += 1
    return cursor_pos

def org_next_elem(max_pos = None):
    global cursor_pos
    if org_cursor_type() == ORG_LINK:
        org_move_after_link()
    elif org_cursor_type() == ORG_WORD:
        org_move_after_word()
    elif org_cursor_type() == ORG_SEP:
        org_move_after_sep()
    elif org_cursor_type() == ORG_EMPTY_LINE:
        org_move_after_empty_line()
    elif org_cursor_type() == ORG_LIST:
        org_move_after_list()
    else:
        cursor_pos +=1
    if max_pos is not None and cursor_pos >= max_pos:
        cursor_pos = max_pos
    return cursor_pos
    
def org_find_end_list():
    global cursor_pos
    pos = cursor_pos
    res = re.search("\n", txt[:pos])
    if res is None:
        pos = 0
    else:
        pos = res.span()[1]
    res = re.search("\d+\.[ ]", txt[pos:])
    if res is None:
        return len(txt)
    pos = res.span()[1]
    
    
def org_eof():
    return cursor_pos >= len(txt)
