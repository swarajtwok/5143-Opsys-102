'''
Command: wc
Function: This command prints the number of lines, words or characters in a file, depending on flags.
Example: "wc filename", "wc -c filename", "wc -lw filename"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the wc function with keyword arguments
def wc(**kwargs):

    Files = FileSystem()

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    file_list = cmd["argument"].split() 
    cwd = Files.getWorkingDirectory()

    # Organizing the flags so that they are in a predictable order.
    if 'l' in cmd["flags"] and 'c' in cmd["flags"] and 'w' in cmd["flags"]:
        cmd["flags"] = 'lwc'
    elif 'l' in cmd["flags"] and 'w' in cmd["flags"]:
        cmd["flags"] = 'lw'
    elif 'w' in cmd["flags"] and 'c' in cmd["flags"]:
        cmd["flags"] = 'wc'
    elif 'l' in cmd["flags"] and 'c' in cmd["flags"]:
        cmd["flags"] = 'lc'
    elif cmd["flags"] == "" or cmd["flags"] == None:
        cmd["flags"] = ''

    contents = ""
    id = Files.getFileId(pid=str(cwd[0]), filename=str(file_list[0]))
    contents = Files.getContent(id)
    filename = str(file_list[0])
    
    # Add character, word, and line counters
    num_char = len(str(contents))
    num_words = len(str(contents).split())
    num_lines = len(str(contents).splitlines())

    total_chars = len(contents)
    total_words = len(contents.split())
    total_lines = len(contents.splitlines())


    if cmd["flags"] == 'c':
        result = f"{total_chars} {filename}"
    elif cmd["flags"] == 'w':
        result = f"{total_words} {filename}"
    elif cmd["flags"] == 'l':
        result = f"{total_lines} {filename}"
    elif cmd["flags"] == 'lw':
        result = f"{total_lines} {total_words} {filename}"
    elif cmd["flags"] == 'wc':
        result = f"{total_words} {total_chars} {filename}"
    elif cmd["flags"] == 'lc':
        result = f"{total_lines} {total_chars} {filename}"
    elif cmd["flags"] == 'lwc':
        result = f"{total_lines} {total_words} {total_chars} {filename}"
    else:
        result = f"{total_lines} {total_words} {total_chars} {filename}"
        
    Files.close_connection()
    return result
    