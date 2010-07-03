#!/usr/bin/python
import os
import sys


command = ""
if len(sys.argv) == 2:
    command = """
    \"(with-current-buffer
    (get-buffer-create \\\"*Piped %s*\\\")
    (switch-to-buffer \\\"*Piped %s*\\\")
    (delete-region (point-min) (point-max)))\"
    """%(sys.argv[1], sys.argv[1])
else:
    command = """
    \"(with-current-buffer
    (get-buffer-create \\\"*Piped*\\\")
    (switch-to-buffer \\\"*Piped*\\\")
    (delete-region (point-min) (point-max)))\"
    """
    
command = command.replace("\n", " ")

#os.execlp("emacsclient", "-e" , "-e",  command)
text = os.popen("emacsclient -e %s"%command).read()


before_print = 1
text = ""
while (1):
    before_print-= 1
    line = sys.stdin.readline()
    if line == '':
        break
    text += line + "\\\\n"
    #manca la regexp per il quoting
    #$foo =~ s/(["\\])/\\$1/g;

    if before_print == 0:
        command = """
        \"(with-current-buffer
        (get-buffer-create \\\"*Piped*\\\")
        (insert \\\"%s\\\")
        )\"
        """%(text)

        command = command.replace("\n", " ")
        #os.execlp("emacsclient", "-e" , "-e",  command)
        text = os.popen("emacsclient -e %s"%command).read()
        text = ""
        before_print = 1
