'''
Command: cat
Function: This command reads one or more files and prints their contents to the standard output.
Example: "cat filename1 filename2", "cat filename1 filename2 > filename3"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the cat function with keyword arguments
def cat(**kwargs):

    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    file_list = cmd["argument"].split() 
#    print(file_list)

    cwd = Files.getWorkingDirectory()[0]
    contents = ""

    # Check if standard input is provided (piping)
    if cmd["input"] != None and cmd["argument"] == "":
        contents = cmd["input"]

    # If there are one or more file names provided
    elif len(file_list) >= 1:
        contents = ""

        # Iterate through the list of file names
        for file_name in file_list:
            file_id = Files.getFileId(pid=str(cwd), filename=str(file_name))
            
            # Read the contents of the file and append to the concatenated contents
            file_contents = Files.getContent(file_id)
            contents += file_contents
            
    # Handle the case where there is no argument or input
    else:
        contents = "Concatenation Error!!"
        
    Files.close_connection()
    return contents
    