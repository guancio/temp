#!/usr/bin/python
import os
import sys


command = ""
if len(sys.argv) == 2:
    command = """
    \"(with-current-buffer
    (get-buffer-create \\\"*Piped %s*\\\")
    (buffer-string)
    )\"
    """%(sys.argv[1])
    command = command.replace("\n", " ")
else:
    command = """
    \"(with-current-buffer
    (get-buffer-create \\\"*Piped*\\\")
    (buffer-string)
    )\"
    """.replace("\n", " ")
    
text = os.popen("emacsclient -e %s"%command).read()
text = eval(text)
print text
