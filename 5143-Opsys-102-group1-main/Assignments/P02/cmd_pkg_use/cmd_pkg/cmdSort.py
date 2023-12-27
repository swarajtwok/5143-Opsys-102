'''
Command: sort
Function: This command alphabetically sorts the lines of a file.
Example: "sort filename", "sort -r filename"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the sort function with keyword arguments
def sort(**kwargs):

    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    # Split the argument into a list of strings
    file_list = cmd["argument"].split() 

    cwd = Files.getWorkingDirectory()

    contents = ""

    filename = str(file_list[0])

    # Get the ID and contents of the specified file
    id = Files.getFileId(pid=str(cwd[0]), filename=str(file_list[0]))
    contents = Files.getContent(id)

    if not contents:
        Files.close_connection()
        return f"File '{filename}' not found."
    
    # Check the sorting flag
    if cmd["flags"] == 'r':
            # Sort the lines in reverse order (alphabetically)
        sorted_lines = sorted(contents.splitlines(), reverse=True)
    else:
        # Sort the lines in regular order (alphabetically)
        sorted_lines = sorted(contents.splitlines())
    
    sorted_contents = "\n".join(sorted_lines)
    Files.close_connection()
    return sorted_contents
    