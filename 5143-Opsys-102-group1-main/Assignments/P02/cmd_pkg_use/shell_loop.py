"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""

# Import necessary libraries and modules
import os
import sys
from fileSystem import FileSystem
from time import sleep
from rich import print
from rich.text import Text


from cmd_pkg import *
from cmd_pkg import CommandsHelper

cmdHelper = CommandsHelper()

##################################################################################

# Define the Getch class for capturing user input
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

# Define the _GetchUnix class for Unix-like systems
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

# Define the _GetchWindows class for Windows systems
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

##################################################################################

# Create instance of our getch class
getch = Getch()                             

# Set default prompt
prompt = "$"                               

# Function to clear the command line and print the current command
def print_cmd(cmd):

    Files = FileSystem()
    padding = " " * 80
    preamble = Files.getWorkingDirectory()[1]
    if preamble == '/':
        preamble = "~"
    colored_preamble = ("\033[93m" + preamble + "\033[0m")
    sys.stdout.write("\r"+padding)
    sys.stdout.write("\r"+colored_preamble+prompt+cmd)
    sys.stdout.flush()
    Files.close_connection()

# Function to parse a command string and create a command dictionary
def command_parser(cmd):
    cmd_raw = cmd.split('>')

    if len(cmd_raw) > 1:
        Input_file = cmd_raw[1].strip()

    Piped_split = cmd_raw[0].split('|')
    cmd_dict = []
    for item in Piped_split:
        terms = item.split()
        item_dictionary = {"command": "", "flags": "", "argument": ""}

        # Special history command
        if len(terms) > 0 and "!" in terms[0]:
            item_dictionary["command"] = "history"
            item_dictionary["argument"] = terms[0].strip("!")
            item_dictionary["flags"] = ""
        else:
            item_dictionary["command"] = terms[0]
            terms.pop(0) 
            for term in terms:
                if term[0] == '-':
                    item_dictionary["flags"] += term[1:]
                else:
                    item_dictionary["argument"] += term + " "
            if item_dictionary["argument"] != "":
                item_dictionary["argument"] = item_dictionary["argument"].strip()
        cmd_dict.append(item_dictionary)
    return cmd_dict

# Main script execution block
if __name__ == '__main__':
    cmd = ""                                # empty cmd variable

    print_cmd(cmd)                          # print to terminal
    
    while True:                             # loop forever

        char = getch()                      # read a character (but don't print)

        if char == '\x03' or cmd == 'exit': # ctrl-c
            print("")
            raise SystemExit()
        
        elif char == '\x7f':                # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)
            
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            
            if direction in 'A':            # up arrow pressed
                cmd += u"\u2191"
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
                
            if direction in 'B':            # down arrow pressed
                cmd += u"\u2193"
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
            
            if direction in 'C':            # right arrow pressed    
                cmd += u"\u2192"
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]

            if direction in 'D':            # left arrow pressed
                cmd += u"\u2190"
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
            
            print_cmd(cmd)                  # print the command (again)

        # Handle return key
        elif char in '\r':                  # return pressed 
            
            fluff = ""   # 
            print(fluff)                  
            sleep(1)    

            Files = FileSystem()

            # Our bhist (bash history) file is ID 3
            Temp_String = Files.getContent(3)
            Temp_String += "\n" + cmd
            Temp_String = Temp_String.strip() 
            Files.chcontent(id = 3, new_value = Temp_String)
            Files.close_connection()
            
            Input_file = None
            cmd_raw = cmd.split('>')

            if len(cmd_raw) > 1:
                Input_file = cmd_raw[1].strip()
            standard_in = None
            result = ""
            cmd_dict = command_parser(cmd)
            for item in cmd_dict:                
                if item["command"] != 'history':
                    if(not cmdHelper.exists(item["command"])):
                        print(f"Command not found, %s" % item["command"])
                        break
                    try:
                        result = cmdHelper.run(item["command"])(flags=item["flags"],argument=item["argument"],input=standard_in)
                    except:
                        result = ""
                        Input_file = None
                    standard_in = result
                elif item["command"] == 'history':
                    if(not cmdHelper.exists(item["command"])):
                        print(f"Command not found, %s" % item["command"])
                        break
                    if(item["argument"] == ""):
                        try:
                            result = cmdHelper.run(item["command"])(flags=item["flags"],argument=item["argument"],input=standard_in)
                        except:
                            result = ""
                            Input_file = None
                    else:
                        try:
                            cmd = cmdHelper.run(item["command"])(flags=item["flags"],argument=item["argument"],input=standard_in, db = Files)
                        except:
                            cmd = "history"
                            Input_file = None
                        if cmd == None:
                            cmd = "history"                    
                        cmd_raw = cmd.split('>') #our output going out to a file
                        if len(cmd_raw) > 1:
                            Input_file = cmd_raw[1].strip()
                        cmd_dict = command_parser(cmd)
                        for item in cmd_dict:                
                            if item["command"] != 'history':
                                if(not cmdHelper.exists(item["command"])):
                                    print(f"Command not found, %s" % item["command"])
                                    break
                                try:
                                    result = cmdHelper.run(item["command"])(flags=item["flags"],argument=item["argument"],input=standard_in)
                                except:
                                    result = ""
                                    Input_file = None
                                standard_in = result
                            elif item["command"] == 'history':
                                if(not cmdHelper.exists(item["command"])):
                                    print(f"Command not found, %s" % item["command"])
                                    break
                                try:
                                    result = cmdHelper.run(item["command"])(flags=item["flags"],argument="",input=standard_in)
                                except:
                                    result = ""

                    standard_in = result
            if Input_file != None:
                try:
                    Files = FileSystem()

                    File_exists = None
                    Path = None
                    File_Name = Input_file
                    if "/" in File_Name:
                        File_Name = File_Name.split("/")
                        File_Name = File_Name.pop(-1)
                        Path = Files.pathParser(cmd_raw[1].strip()[:-len(File_Name)])
                        File_exists = Files.getFileId(pid = Path,filename = File_Name)
                    else:
                        Path = Files.getWorkingDirectory()[0]
                        File_exists = Files.getFileId(pid = Path, filename = File_Name)
                    if File_exists == []:
                        Files.insert_data((Path, File_Name, "file",25,"root","root","-rwxrwxrwx","2023-04-03 00:00:00",str(result),"0"))
                    elif File_exists != []:
                        Files.chcontent(id = File_exists, new_value = str(result))
                    else:
                        pass
                    
                    pass
                except:
                    print("Redirect file does not exist")
            else:
                if result != None:
                    print(f"{result}")



            cmd = ""                        # reset command to nothing (since we just executed it)

            print_cmd(cmd)                  # now print empty cmd prompt
        else:
            cmd += char                     # add typed character to our "cmd"
            print_cmd(cmd)                  # print the cmd out