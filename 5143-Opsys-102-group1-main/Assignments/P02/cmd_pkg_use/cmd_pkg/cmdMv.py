'''
Command: mv
Function: This command is used to move or rename files .
Example: "mv filename1 filename2" "mv filename dirname"
'''

#!/usr/bin/env python
from fileSystem import FileSystem
def mv(**kwargs):
    cmd = {}

    for key, item in kwargs.items():
        cmd.update({key: item})

    Files = FileSystem()

    # Separating my files to copy and where to send it
    arg_list = cmd["argument"].split()

    # Destination files, where we are sending the files to
    Destination = arg_list[-1]
    
    # Removing the destination from the arg_list 
    # to process the list later as just the source files
    arg_list.pop()
    Destination_File = ""
    Destination_pid = ""

    Source = []
    Source_File = []
    Source_pid = []

    # Adding every remaining argument to the source list
    for item in arg_list:
        Source.append(item)

    # Parsing through the Source list to get the file names and pids
    for item in Source:
        if "/" in item:
            Path_Placeholder = item.split("/")

            # Source is a file
            if Files.pathParser(item) == None:
                Source_File.append(Path_Placeholder[-1])
                item = item[:-(len(Path_Placeholder[-1]))]
                Source_pid.append(Files.pathParser(item))
            # Source is a directory
            else:
                Source_pid.append(Files.pathParser(item))
                Source_File.append(item)
        else:
            if Files.pathParser(item) == None:
                Source_pid.append(Files.getWorkingDirectory()[0])
                Source_File.append(item)
            else:
                Source_pid.append(Files.pathParser(item))
                Source_File.append(item)

    # Checking if the Destination is a directory or a file.
    Destination_Placeholder = Files.pathParser(Destination)
 
    # Parsing the Destination to get the pid and the file name
    if "/" in Destination:
        Path_Placeholder = Destination.split("/")
        if Destination_Placeholder == None and len(Source) == 1:
            Destination_File = Path_Placeholder[-1]
            Destination = Destination[:-(len(Destination_File))]
            Destination_pid = Files.pathParser(Destination[:])
        elif Destination_Placeholder == None and len(Source) > 1:
            print(f"cp: '{str(Path_Placeholder[-1])}' is not a directory.\n")
            return None
        else:
            Destination_pid = Files.pathParser(Destination)
            Destination_File = None
    else:
        # If it is a file
        if Files.pathParser(Destination) == None:
            Destination_pid = Files.getWorkingDirectory()[0]
            Destination_File = Destination[:]
            # If Destination is a directory that does not exist
        elif len(Source) == 1 and Files.getFile(Files.pathParser(Destination)) == None:
            Placeholder_list = Destination.split("/")
            Destination_File = Placeholder_list[-1]
            Destination = Destination[:-(len(Destination_File))]
            Destination_pid = Files.pathParser(Destination)
        else:
            Destination_pid = Files.pathParser(Destination)
            Destination_File = None

    ''' We have a few use cases to go through.
    #1. we have 1 source file/directory and 1 destination file.
    #2. we have 1 source file/directory and 1 destination directory.
    #3. we have 1+ source files/directories and 1 destination directory.
    # Thanks to error checking in the destination parsing area we know that if we have more than 1 source file, our destination
    # must be a directory.
    '''

    for item in Source_File:
        location = 0
        temp_name = item[:]
        Directory_Flag = 0
        if Destination_File == None:
            temp = Files.getFileId(pid = Source_pid[location], filename = str(item))
            if (temp == [] or temp == None) and Files.pathParser(item) != None:
                temp = Source_pid[location]
                temp_name = item.split("/")[-1]
                Directory_Flag = 1
            temp_tuple = Files.getFile(temp)
            temp_tuple = temp_tuple[3:]
            temp_tuple = (Destination_pid,temp_name) + temp_tuple
            Files.chpid(id = temp,new_value = temp_tuple[0])

        else:
            temp = Files.getFileId(pid = Source_pid[location], filename = str(item))
            if (temp == [] or temp == None) and (Files.pathParser(Destination_pid) != None or Files.pathParser(Destination_pid) != None):
                print("mv: cannot overwrite non-directory with directory")
            else:
                ID = Files.getFile(temp)[0]
                Tuple = Files.getFile(temp)
                Temp_Tuple = Tuple[3:]
                Temp_Tuple = (Destination_pid,Destination_File) + Temp_Tuple
                Files.insert_data(Temp_Tuple)
                Files.remove_data(str(ID))
        location += 1

    # Close the connection
    Files.close_connection()