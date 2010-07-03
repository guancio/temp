#!/usr/bin/python
import os
import sys


text = ""
while (1):
    line = sys.stdin.readline()
    if line == '':
        break
    text += line
    #manca la regexp per il quoting
    #$foo =~ s/(["\\])/\\$1/g;

command = ""
if len(sys.argv) == 2:
    command = """
    (with-current-buffer
    (get-buffer-create \"*Piped %s*\")
    (switch-to-buffer \"*Piped %s*\")
    (delete-region (point-min) (point-max))
    (insert \"%s\"))
    """%(sys.argv[1], sys.argv[1], text)
else:
    command = """
    (with-current-buffer
    (get-buffer-create \"*Piped*\")
    (switch-to-buffer \"*Piped*\")
    (delete-region (point-min) (point-max))
    (insert \"%s\"))
    """%(text)
    

os.execlp("emacsclient", "-e" , "-e",  command)
