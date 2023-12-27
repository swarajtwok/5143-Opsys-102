'''
Command: echo
Function: This command prints to standard output the text that is passed as an argument.
Example: "echo Hello", "echo Hello > filename"
'''

#!/usr/bin/env python
from fileSystem import FileSystem


def echo(**kwargs):

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    if cmd["argument"] != "":
        if cmd["argument"][0] == '"' and cmd["argument"][-1] == '"':
            cmd["argument"] = cmd["argument"][1:-1]
        return cmd["argument"]
    elif cmd["input"] != "":
        if cmd["input"][0] == '"' and cmd["input"][-1] == '"':
            cmd["input"] = cmd["input"][1:-1]
        return cmd["input"]
    else:
        print("echo: missing argument")
        return None