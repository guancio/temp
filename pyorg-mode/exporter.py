import parser

reload(parser)


body = ""
current_p = None
current_ul = None
end_block = None

while not parser.org_eof():
    if current_p is not None and  parser.org_cursor_type() == parser.ORG_EMPTY_LINE:
        body += '</p>'
        current_p = None
    elif current_p is None:
        current_p = 1
        body += '<p>'

    if current_ul is not None and  parser.cursor_pos > current_ul:
        body += '</ul>'
    if parser.org_cursor_type() == parser.ORG_EMPTY_LINE:
        current_ul = parser.org_find_end_list()
        body += '<p>'

    if parser.org_cursor_type() == parser.ORG_LINK:
        link, title = parser.org_parse_link()
        body += '<a href="%s">%s</a>'% (link, title)
    if parser.org_cursor_type() == parser.ORG_WORD:
        body += '%s' % parser.org_parse_word()
    if parser.org_cursor_type() == parser.ORG_SEP:
        body += '%s' % parser.org_parse_sep()

    if parser.org_cursor_type() == parser.ORG_EMPTY_LINE:
        pass
    
    if parser.org_cursor_type() == parser.ORG_LIST:
        body += '<li>'

    parser.org_next_elem(end_block)

text = open("template.html").read().replace("DOCUMENT_BODY", body)
out = open("netfarm.html", "w")
out.write(text)
out.close()
