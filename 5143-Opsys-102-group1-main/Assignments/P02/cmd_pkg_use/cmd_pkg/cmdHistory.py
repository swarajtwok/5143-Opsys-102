'''
Command: history
Function: This command prints a numbered list of all the previous user command to the shell.
Example: "history"
'''

#!/usr/bin/env python
import subprocess
import readline; 
from fileSystem import FileSystem

# Define the mkdir function with keyword arguments
def history(**kwargs):

    Files = FileSystem()
    # History is saved in a file called bhist (id=3)
    History = Files.getContent("3")
    Output = History.split('\n')
    i = 0

    # If no arguments, we just print off the history
    if kwargs["argument"] == "":
        temp = ""
        for Line in Output:
            temp += str(i) + " " + Line + "\n"
            i += 1
        return temp
    else:
        try:
            # If we have an argument, we need to parse it.
            temp = Output[int(kwargs["argument"])]
            return temp
        except: 
            print("Error: invalid command number.")

    Files.close_connection()

if __name__=='__main__':
    print("\n")
    history()