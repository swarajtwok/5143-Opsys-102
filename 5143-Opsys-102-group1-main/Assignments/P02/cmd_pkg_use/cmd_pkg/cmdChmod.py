'''
Command: chmod
Function: This command changes the permissions (mode) of files and directories depending 
on provided permissions from 000 to 777.
Example: "chmod 777 dirname"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the chmod function with keyword arguments
def chmod(**kwargs):

    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    '''Note: Due to the nature of our splits a permission that starts with '-' will 
             falsely be read in as a flag. This is a workaround to fix that.'''

    if len(cmd["flags"]) > 5:

        # Split the flags so we do no accidentally add a true flag to the argument.
        temp_split = cmd["flags"].split()
        for item in temp_split:
            # Only strings in flags of more than size 5 should be permissions
            if len(item) > 5:
                # Add the '-' back to the permission and make it a proper argument
                cmd["argument"] = "-" + item + " " + cmd["argument"]
                # Remove the permission from the flags
                cmd["flags"] = cmd["flags"].replace(item, "")

    # Split the argument into a list of strings
    argument_list = cmd["argument"].split()
    path = argument_list[1]
    perm = argument_list[0]

    # Pathparser doesn't read files, only directories.
    id = Files.pathParser(path)
    
    # If the path is not a directory, it's a file
    if id == None:
        temp_filename = path.split("/").pop(-1)
        path = path[:-(len(temp_filename))]
        print(path)
        id = Files.getFileId(filename=temp_filename, pid=path)
    Files.chmod(id=id, permission=perm)