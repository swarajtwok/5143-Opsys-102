'''
Command: ls
Function: This command lists directories and files in the current working direcotry.
Example: "ls -lah", "ls"
'''

#!/usr/bin/env python

from fileSystem import FileSystem

def ls(**kwargs):

    cmd = {}

    for key, item in kwargs.items():
        cmd.update({key:item})

    Files = FileSystem()
    file_list = []
    id = Files.pathParser(cmd['argument'])
    current_file = Files.getFile(id)
    if cmd["flags"] != "" and "a" in cmd["flags"]:
        if current_file[1] != 0:
            parent_id = current_file[1]
            parent_file = Files.getFile(parent_id)
        else:
            parent_file = None
        Temp_String = "."
        current_file = current_file[0:2] + (Temp_String,) + current_file[3:]
        file_list.append(current_file)
        if parent_file != None:
            Temp_String = ".."
            parent_file = parent_file[0:2] + (Temp_String,) + parent_file[3:]
            file_list.append(parent_file)

    list_list = Files.list(pid = id)

    for item in list_list:
        file_list.append(item)


    if cmd["argument"] is None:
        print("LS call Invalid argument")   

    # Organizing the flags so that they are in a predictable order.
    if 'a' in cmd["flags"] and 'l' in cmd["flags"] and 'h' in cmd["flags"]:
        cmd["flags"] = 'lah'
    elif 'a' in cmd["flags"] and 'l' in cmd["flags"]:
        cmd["flags"] = 'al'
    elif 'a' in cmd["flags"] and 'h' in cmd["flags"]:
        cmd["flags"] = 'ah'
    elif 'l' in cmd["flags"] and 'h' in cmd["flags"]:
        cmd["flags"] = 'lh'
    elif cmd["flags"] == "" or cmd["flags"] == None:
        cmd["flags"] = ''
    elif "a" in cmd["flags"] or "l" in cmd["flags"] or "h" in cmd["flags"]:
        cmd["flags"] = cmd["flags"]
    else:
        print("Invalid flags")

# Format the output as needed
    output = ""
    def bytes_to_human(bytes):
        units = ['B', 'KB', 'MB']
        unit_index = 0
        
        while bytes >= 1024 and unit_index < len(units) - 1:
            bytes /= 1024.0
            unit_index += 1
        result = f"{int(bytes)}{units[unit_index]}"
        
        return result
    
    max_length = 0  # Initialize max_length to 0


    for item in file_list:
        filename = item[2]
        if "/" in filename:
            temp_string = filename.split("/")[-1]
            filename = "[green]" + temp_string + "[/green]"
        elif filename == "." or filename == "..":
            filename = "[green]" + filename + "[/green]"
        file_type = item[3]  
        filesize = str(item[4])
        filesize_human = bytes_to_human(item[4])
        owner = item[5]
        group_name = item[6]
        permissions = item [7]
        date_modified = item[8]
        date_modified2 = date_modified[5:16]



        line_length = 120  # The desired line length
        
        # Handle the output based on input flags
        if cmd["flags"] == 'lah':
            output += f"{permissions.ljust(14)} {owner.ljust(6)} {group_name.ljust(6)} {filesize_human.ljust(5)} {date_modified2.ljust(max_length)} {filename.ljust(20)}\n"
        elif cmd["flags"] == 'al':
            output += f"{permissions.ljust(12)} {owner.ljust(6)} {group_name.ljust(6)} {filesize.ljust(5)} {date_modified2.ljust(10)} {filename.ljust(20)}\n"
        elif cmd["flags"] == 'ah':
            output += f"{filename.ljust(12)}"
        elif cmd["flags"] == 'lh':
            output += f"{permissions.ljust(12)} {owner.ljust(6)} {group_name.ljust(6)} {filesize_human.ljust(5)} {date_modified2.ljust(10)} {filename.ljust(20)}\n"
        elif cmd["flags"] == 'l':
            output += f"{permissions.ljust(12)} {owner.ljust(6)} {group_name.ljust(6)} {filesize.ljust(5)} {date_modified2.ljust(10)} {filename.ljust(20)}\n"
        elif cmd["flags"] == 'a':
            if len(output) + len(filename) > line_length:
                output += "\n"
            output += f"{filename.ljust(7)}" + " "
        elif cmd["flags"] == 'h':
            if len(output) + len(filename) > line_length:
                output += "\n"
            output += f"{filename.ljust(7)}"
        else:
            if len(output) + len(filename) > line_length:
                output += "\n"
            output += f"{filename.ljust(7)}" + " "

    Files.close_connection()
    return output
