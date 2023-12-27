'''
Command: mkdir
Function: This command creates a directory or a subdirectory of the argument name.
Example: "mkdir directory"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the mkdir function with keyword arguments
def mkdir(**kwargs):

    Files = FileSystem()
    Hidden = 0

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})
    cmd["argument"] = cmd["argument"].strip()

    # Check if the argument contains a slash ("/"), indicating a directory path
    if "/" in cmd["argument"]:
        Path_Placeholder = cmd["argument"].split("/")
        Final_Directory = Path_Placeholder[-1]

        # Check if the final directory name starts with a dot (hidden directory)
        if Final_Directory[0] == ".":
            Hidden = 1
        cmd["argument"] = cmd["argument"][:-(len(Final_Directory))]

        # Parse the path and get the ID of the specified directory
        Path = Files.pathParser(cmd["argument"])

        Files.insert_data((Path,str(Final_Directory), "Directory", 0, "root", "root", "drwxrwxrwx", "2021-04-03 00:00:00", None, str(Hidden)))


    else:
        # Check if the argument starts with a dot (hidden directory)
        if cmd["argument"][0] == ".":
            Hidden = 1
        Files.insert_data((Files.getWorkingDirectory()[0],cmd["argument"], "Directory", 0, "root", "root", "drwxrwxrwx", "2021-04-03 00:00:00", None, str(Hidden)))
