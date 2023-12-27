import re

def PipetoDictionary(raw_string):
    cmd_dict = {"command":'', "flags":'',"argument":''}    
    #Now to split on the pipes
    Pipe_Placeholder = raw_string.split('|')
    stripped_list = [s.strip() for s in Pipe_Placeholder]
    #print(stripped_list)

    #now for the regex.
    command_pattern = r'\b([a-zA-Z]+)'
    flag_pattern = r'\W-([a-zA-Z]+)'
    #argument_pattern = r'(?<=\s)(?![\w-]*\s)?(\w+)'
    #updated argument pattern to account for double quotes for gretch implementation.
    argument_pattern = r'(?<=\s)(?![\w-]*\s)-?("[^"]+"|\w+)'
    command_list = []

    for item in stripped_list:
        command_match = re.search(command_pattern,item)
        flag_match = re.findall(flag_pattern,item)
        argument_match = re.findall(argument_pattern,item)
        if command_match:
            cmd_dict["command"] = command_match.group(1)
        if flag_match:
            for item in flag_match:
                cmd_dict["flags"] += item
        if argument_match:
            for item in argument_match:
                cmd_dict["argument"] += item
        command_list.append({"command":cmd_dict["command"], "flags":cmd_dict["flags"],"argument":cmd_dict["argument"]})
    return command_list
    
if __name__ == "__main__":
    Input_String = "ls -lah prune orange -a -l apple -h candy | getch cookies | history > outfile.txt"

    #we will want to remove the > and <
    #will need to implement the other at some point
    Split_Placeholder = Input_String.split('>')

    #print(Split_Placeholder)

    Outfile = Split_Placeholder[1].strip()
    #print(Outfile)

    #now to work on processing the cmds.
    #We want to plug them into the dictionary below.
    cmd_dict = {"command":"", "flags":"","argument":""}

    #Now to split on the pipes
    Pipe_Placeholder = Split_Placeholder[0].split('|')
    stripped_list = [s.strip() for s in Pipe_Placeholder]
    #print(stripped_list)

    #now for the regex.
    command_pattern = r'\b([a-zA-Z]+)'
    flag_pattern = r'\W-([a-zA-Z]+)'
    argument_pattern = r'(?<=\s)(?![\w-]*\s)?(\w+)'

    print(stripped_list[0])
    #command RE
    match = re.search(command_pattern,stripped_list[0])
    #Command = match.group(1)
    #print(Command)
    print(match.group(1))
    #flag RE
    print("Flag captures:")
    match = re.findall(flag_pattern,stripped_list[0])
    for item in match:
        print(item)
    #print(match.group(1))
    #argument RE
    #has issues with words like "or-ange" will capture "or"
    print("Argument captures:")
    match = re.findall(argument_pattern,stripped_list[0])
    for item in match:
        print(item)

