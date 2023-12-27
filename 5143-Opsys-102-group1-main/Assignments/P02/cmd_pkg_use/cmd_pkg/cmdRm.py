'''
Command: rm
Function: This command removes a file or directory (including files in it).
Example: "rm filename", "rm -rf dirname"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the rm function with keyword arguments
def rm(**kwargs):

    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    Source = cmd["argument"].split()
    Source_Path = []
    Source_Name = []

    # Iterate through the provided sources (files or directories)
    for item in Source:
        if "/" in item:
            # Check if it is a directory or a file/nonexistent item.
            if Files.pathParser(item) == None:
                # This catches non existent files and directories.
                Temp_Name = item.split("/")[-1]
                Temp_Path_Name = item[:-len(Temp_Name)]
                if Files.getFileId(pid = Files.pathParser(Temp_Path_Name), filename = str(Temp_Name)) == [] or Files.getFileId(pid = Files.pathParser(Temp_Path_Name), filename = str(Temp_Name)) == None:
                    print("rm: cannot remove '" + item + "': No such file or directory")
                    return
                # The item is a file and it exists.
                Name_Placeholder = item.split("/")[-1]
                Source_Name.append(Name_Placeholder)
                Source_Path.append(Files.pathParser(item[:-len(Name_Placeholder)]))
            else:
                Source_Path.append(Files.pathParser(item))
                Source_Name.append("")
        # It is a directory.
        else:
            # Check if the name leads to a directory or to a file.
            if Files.pathParser(item) == None:
                # This catches non existent files and directories.
                if Files.getFileId(pid = Files.getWorkingDirectory()[0], filename = str(item)) == [] or Files.getFileId(pid = Files.getWorkingDirectory()[0], filename = str(item)) == None:
                    print("rm: cannot remove '" + item + "': No such file or directory")
                    return
                # The item is a file and it exists.
                Source_Name.append(item)
                Source_Path.append(Files.getWorkingDirectory()[0])
                # The item is a directory.
            else:
                Source_Path.append(Files.pathParser(item))
                Source_Name.append("")

    # To remove a directory, use -rf flags
    if "r" in cmd["flags"] and "f" in cmd["flags"]:
        Destination = 0
        for item in Source:
            # If it is a directory
            if Source_Name[Destination] == "":
                Children = Files.list(pid = Source_Path[Destination])
                if len(Children) != 0:
                    for item in Children:
                        New_Path = Files.getFile(Source_Path[Destination])[2]
                        rm(argument = str(New_Path) + "/"+ str(item[2]), flags = "rf", input = "")
                Files.remove_data(Source_Path[Destination])
            else:
                # Use our path and filename to get the ID of our file before we delete it.
                File_Id = Files.getFileId(pid = Source_Path[Destination], filename = Source_Name[Destination])
                Files.remove_data(File_Id)

            Destination += 1
    else:
        Destination = 0
        for item in Source:
            # If it is a directory
            if Source_Name[Destination] == "":
                print("rm: cannot remove '" + item + "': Is a directory")
                return
            else:
                # Use our path and filename to get the ID of our file before we delete it.
                File_Id = Files.getFileId(pid = Source_Path[Destination], filename = Source_Name[Destination])
                Files.remove_data(File_Id)

            Destination += 1