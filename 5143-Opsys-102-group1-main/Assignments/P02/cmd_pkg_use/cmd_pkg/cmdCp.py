'''
Command: cp
Function: This command prints full path of the current/working directory.
Example: "pwd"
'''

#!/usr/bin/env python
from fileSystem import FileSystem

# Define the cp function with keyword arguments
def cp(**kwargs):
    cmd = {}

    for key, item in kwargs.items():
        cmd.update({key: item})

    Files = FileSystem()

    # Separating my files to copy and where to send it.
    arg_list = cmd["argument"].split()

    # Destination files, where we are sending the files to.
    Destination = arg_list[-1]

    # Removing the destination from the arg_list to process the list later as just the source files.
    arg_list.pop()
    Destination_File = ""
    Destination_pid = ""

    # Source files, files we are copying have to be a list.
    Source = []
    Source_File = []
    Source_pid = []

    # Adding every remaining argument to the source list
    for item in arg_list:
        Source.append(item)

    # Parsing through the Source list to get the file names and pids.
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
    #now to parse the Destination to get the pid and the file name.
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
        #if it is a file
        if Files.pathParser(Destination) == None:
            Destination_pid = Files.getWorkingDirectory()[0]
            Destination_File = Destination[:]
        elif len(Source) == 1 and Files.getFile(Files.pathParser(Destination)) == None:
            Placeholder_list = Destination.split("/")
            Destination_File = Placeholder_list[-1]
            Destination = Destination[:-(len(Destination_File))]
            Destination_pid = Files.pathParser(Destination)
        #if it is a directory
        else:
            Destination_pid = Files.pathParser(Destination)
            Destination_File = None

    ''' We have a few use cases to go through.
    #1. we have 1 source file/directory and 1 destination file.
    #2. we have 1 source file/directory and 1 destination directory.
    #3. we have 1+ source files/directories and 1 destination directory.
    Thanks to error checking in the destination parsing area we know that if we have more than 1 source file, our destination 
    must be a directory.
    '''

    for item in Source_File:
        location = 0
        temp_name = item[:]
        Directory_Flag = 0
        #our destination is a directory, so this is not a rename just a copy.
        if Destination_File == None:
            temp = Files.getFileId(pid = Source_pid[location], filename = str(item))
            # Source is a directory
            if temp == [] or temp == None:
                temp = Source_pid[location]
                temp_name = item.split("/")[-1]
                Directory_Flag = 1
            temp_tuple = Files.getFile(temp)
            # Removing the id and pid from the tuple.
            temp_tuple = temp_tuple[3:]
            # Adding the new pid to the tuple.
            temp_tuple = (Destination_pid,temp_name) + temp_tuple
            Files.insert_data(temp_tuple)

            if(Directory_Flag == 1):
                # We need to get the id of the directory we just inserted.
                temp = Files.pathParser(Destination + "/" + temp_name)
                temp_files = Files.list(pid = temp)
                # We need to copy all the files in the directory.
                for file in temp_files:
                    temp_tuple = Files.getFile(file[0])
                    # Now we recursively call cp on each file/directory in the directory.
                    cp(argument = str(temp_tuple[2]) + " " + Destination + "/" + temp_name , flags = "", input = "")
        # Our destination is a file, so this is a rename and/or move.
        # Source can never be a directory here.
        else:
            temp = Files.getFileId(pid = Source_pid[location], filename = str(item))
            if temp == [] or temp == None:
                temp = Source_pid[location]
                temp_name = item.split("/")[-1]
                Directory_Flag = 1

            if len(Source) == 1 and Files.getFile(Destination_pid) == None and Directory_Flag == 1:
                dir_temp_tuple = temp_tuple[3:]
            else:
                pass
            temp_tuple = Files.getFile(temp)
            temp_tuple = temp_tuple[3:]
            temp_tuple = (Destination_pid,str(Destination_File)) + temp_tuple
            Files.insert_data(temp_tuple)
        location += 1


    # Close the connection
    Files.close_connection()

# Sample call for demonstration
# (Note: This is just a structured code; actual execution might require additional adjustments based on the FileSystem class implementation.)
# output = copy(source="/path/to/source/file.txt", destination="/path/to/destination/directory/")
