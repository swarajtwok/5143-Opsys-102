import os,sys

# sys.path.append(os.getcwd())

from cmd_pkg.cmdLs import ls
from cmd_pkg.cmdPwd import pwd
from cmd_pkg.cmdCat import cat
from cmd_pkg.cmdHead import head
from cmd_pkg.cmdMkdir import mkdir
from cmd_pkg.cmdGrep import grep
from cmd_pkg.cmdExit import exit
from cmd_pkg.cmdWc import wc
from cmd_pkg.cmdSort import sort
from cmd_pkg.cmdGrep import grep
from cmd_pkg.cmdCd import cd
from cmd_pkg.cmdChmod import chmod
from cmd_pkg.cmdHistory import history
from cmd_pkg.cmdTail import tail
from cmd_pkg.cmdCp import cp
from cmd_pkg.cmdTouch import touch
from cmd_pkg.cmdEcho import echo
from cmd_pkg.cmdRm import rm
from cmd_pkg.cmdMv import mv
from cmd_pkg.cmdLess import less

class CommandsHelper(object):
    """
    This function iterates over globals.items() and if one of the values is "callable"
    meaning it is a function, then I add it to a dictionary called 'invoke'. I also
    add the functions '__doc__' string to a help dictionary.

    Methods:
        exists (string) : checks if a command exists (dictionary points to the function)
        help (string) : returns the doc string for a function 
    """
    def __init__(self):
        self.invoke = {}
        self.help = {}

        for key, value in globals().items():
            if key != 'Commands' and callable(value):
                self.invoke[key] = value
                self.help[key] = value.__doc__

    def exists(self,cmd):
        return cmd in self.invoke
    
    def run(self,cmd):
        if self.exists(cmd):
            return self.invoke[cmd]
    
    def help(self,cmd):
        if self.exists(cmd):
            return self.help[cmd]
        

if __name__=='__main__':
    print("hello")
    print(os.getcwd())
    print(globals().items())
