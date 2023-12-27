'''
Command: grep
Function: This command searches in files for matching string and returns output based on the flags.
Example: grep "Apples" apples
'''

#!/usr/bin/env python
from fileSystem import FileSystem
import re

# Define the grep function with keyword arguments
def grep(**kwargs):

    Files = FileSystem()
    matching_lines = []

    cmd = {}
    for key, item in kwargs.items():
        cmd.update({key:item})

    file_list = cmd["argument"].split() 

    # Initialize variables for the filename, pattern, contents, and path
    filename = ""
    pattern = "" 
    contents = ""
    path = ""

    # If arguments contain both the pattern and the filename
    if len(file_list) >= 2:
        for item in file_list:
            if item[0] == '"' and item[-1] == '"':
                pattern = item[1:-1]
            else:
                filename = item

    # If arguments contain only the pattern and we have a pipped input
    elif len(file_list) == 1 and cmd["input"] != "":
        pattern = str(file_list[0])[1:-1]
        contents = cmd["input"]
    else:
        print("grep: missing filename")
        return None

    # Colors for our text strings
    red_text = "[bold red]"
    reset_color = "[/bold red]"

    if filename != "":
        path = filename[:]
        filename = filename.split('/')[-1]
        path = path[:-len(filename)]
        id = Files.getFileId(pid=str(path),filename=filename)
        contents = Files.getContent(id)

    # Search for matching lines in a case-sensitive manner
    if cmd["flags"] != "i":
        matching_lines = [line for line in contents.split('\n') if pattern in line]
        result = ""
        for line in matching_lines:
            result += line + '\n'
        colored_text = result.replace(pattern, f"{red_text}{pattern}{reset_color}")
        result = f"{colored_text}"
        Files.close_connection()
        return result

    # Search for matching lines in a case-insensitive manner
    else:
        result = ""
        result_string = re.sub(pattern, f"{red_text}{pattern}{reset_color}", contents, flags=re.IGNORECASE)
        pattern = "[bold red]" + pattern + "[/bold red]"
        matching_lines = [line for line in result_string.split('\n') if pattern in line]
        for line in matching_lines:
            result += line + '\n'
        Files.close_connection()
        return result 
