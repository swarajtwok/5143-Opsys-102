'''
Command: less
Function: This command shows file's contents one page at a time.
Example: "less filename"
Keys: Use 'q' to break the command, '-' for line numbering, 
      'j,k' to move up/down 1 line, 'b,spacbar' to move up/down 5 lines.
'''

#!/usr/bin/env python
from fileSystem import FileSystem
import os
import sys

# Gets a single character from standard input.  Does not echo to the screen
class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): 
        return self.impl()

# Define a class to get a single character on Unix systems
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Define a class to get a single character on Windows systems
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

# Define the less function with keyword arguments
def less(**kwargs):
    getch = Getch()
    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})
    
    if "/" in cmd["argument"]:
        file_name = cmd["argument"].split()[-1]
        cwd = Files.pathParser(cmd["argument"][:-len(file_name)]) 
    else:
        cwd = Files.getWorkingDirectory()[0]
        file_name = cmd["argument"]

    contents = ""
    if file_name != "":
        id = Files.getFileId(pid=cwd, filename=str(file_name))
        contents = Files.getContent(id)
    elif cmd["input"] != "":
        contents = cmd["input"]

    maxlines = len(contents.split('\n'))
    Position = 0
    Toggle_Line_Numbers = False
    while True:
        if Toggle_Line_Numbers:
            Number_line = 0 + Position
            for line in contents.split('\n')[Position:Position+5]:
                formatnumber = "\033[31m" + str(Number_line) + ".\033[0m"
                print(f"{formatnumber} {line}")
                Number_line += 1
        else:
            for line in contents.split('\n')[Position:Position+5]:
                print(line)
        char = getch()

        # Break out of the command
        if char == 'q':
            break

        # Page up and down 5 lines
        elif char == ' ':
            Position += 5
            if Position > maxlines - 5:
                Position = maxlines - 5
            #page up
        elif char == 'b':
            Position -= 5
            if Position < 0:
                Position = 0

        # Page up and down 1 line
        elif char == 'j':
            Position += 1
            if Position > maxlines - 5:
                Position = maxlines - 5
        elif char == 'k':
            Position -= 1
            if Position < 0:
                Position = 0

        # Toggle line numbering
        elif char == '-':
            Toggle_Line_Numbers = not Toggle_Line_Numbers
        else:
            pass
        
        # Our print window is 5 lines
        print(f"\033c")
    Files.close_connection()
    