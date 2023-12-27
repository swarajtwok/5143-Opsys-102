'''
Command: cd
Function: This command changes the current working directory depending on the argument provided.
Example: "cd .." "cd directory" "cd ~"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the cd function with keyword arguments
def cd(**kwargs):

    Files = FileSystem()

    cmd = {}

    # Update the dictionary with the keyword arguments provided
    for key, item in kwargs.items():
        cmd.update({key:item})

    # Parse the argument to get the ID of the specified directory
    id = Files.pathParser(cmd["argument"]) 
    Files.chdir(ID=id)

    # Get the current working directory after the change
    cwd = Files.getWorkingDirectory()

    # Set the working directory to the new value
    Files.setWorkingDirectory(cwd[0])
    
    Files.close_connection()