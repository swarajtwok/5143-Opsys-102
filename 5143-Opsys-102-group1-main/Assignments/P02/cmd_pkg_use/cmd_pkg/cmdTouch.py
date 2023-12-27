'''
Command: touch
Function: This command creates a file in the database.
Example: "touch filename"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the mkdir function with keyword arguments
def touch(**kwargs):

    Files = FileSystem()
    Hidden = 0
    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})
    
    # Remove leading and trailing whitespace from the argument
    cmd["argument"] = cmd["argument"].strip()
    for item in cmd["argument"].split():
        # Check if the argument ends with a slash, which is not allowed
        if item[-1] == "/":
            print("touch: setting times of '" + item + "': No such file or directory")
            return None
        
        # Check if the argument contains a slash ("/"), indicating a directory path
        if "/" in item:
            Path_Placeholder = item.split("/")
            Final_File = Path_Placeholder[-1]
            
            # Check if the final file name starts with a dot (hidden file)
            if Final_File[0] == ".":
                Hidden = 1
            item = item[:-(len(Final_File))]

            Path = Files.pathParser(item)
        
            # Insert data for the new file into the file system
            Files.insert_data((Path,str(Final_File), "File", 0, "root", "root", "drwxrwxrwx", "2021-04-03 00:00:00", "", str(Hidden)))
        
        else:
            if item[0] == ".":
                Hidden = 1
            Files.insert_data((Files.getWorkingDirectory()[0],item, "File", 0, "root", "root", "drwxrwxrwx", "2021-04-03 00:00:00", "", str(Hidden)))
