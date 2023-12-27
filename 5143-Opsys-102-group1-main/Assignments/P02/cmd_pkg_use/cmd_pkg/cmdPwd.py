'''
Command: pwd
Function: This command prints full path of the current/working directory.
Example: "pwd"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the pwd function with keyword arguments
def pwd(**kwargs):

    # Call the pathParser method to get the current working directory
    Files = FileSystem()
    current_directory = Files.getWorkingDirectory()[1]

    # Print the current working directory (equivalent to the "pwd" command)
    Files.close_connection()
    return current_directory
