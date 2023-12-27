'''
Command: tail
Function: This command prints the last few lines of a file to standard output.
Example: "tail filename", "tail -n 5 filename"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the tail function with keyword arguments
def tail(**kwargs):

    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    file_list = cmd["argument"].split()

    # Split the content into lines
    contents1 = ""
    contents = ""

    # Check if standard input is provided and flags are used or no argument is given
    if cmd["input"] != None and ((cmd["flags"] !="" and len(cmd["argument"].split()) == 1 and type(cmd["argument"]) is int) or (cmd["flags"] == "" and cmd["argument"] == "")):
        lines = cmd["input"].split('\n')
        if 'n' in cmd["flags"]:
            for line in lines[int(file_list[0]):]:
                contents += line + "\n"
        else:
            for line in lines[-10:]:
                contents += line + "\n"  # Default    

    # If standard in is not being used then we read the files
    else: 

        if cmd["flags"] == "":
            file_list.append(file_list[0])

        # Get the current working directory and the final file name
        cwd = Files.getWorkingDirectory()
        Path_Placeholder = file_list[1].split("/")
        Final_File = Path_Placeholder[-1]
        file_list[1] = file_list[1][:-(len(Final_File))]
        cwd = Files.pathParser(file_list[1])

        # Get the file ID of the specified file
        id = Files.getFileId(pid=str(cwd), filename=str(Final_File))
        contents1 = Files.getContent(id)
        lines = str(contents1).split('\n')

 
        # Check if the 'n' flag is used to specify the number of lines
        if 'n' in cmd["flags"]:
            Line_Count = int(file_list[0])
            for line in lines[-int(Line_Count):]:
                contents += line + "\n"
        else:
            for line in lines[-10:]:
                contents += line + "\n"  # Default


    Files.close_connection()
    return contents
    