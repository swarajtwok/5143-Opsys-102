# Filesystem Starter Class

from sqliteCRUD import SQLiteCRUD
import sqlite3
import datetime

def convert_digit(digit):
    """
    Convert a single digit (0-7) into its 'rwx' equivalent.

    Args:
        digit (int): A single digit (0-7).

    Returns:
        str: The 'rwx' equivalent representation.
    """
    if digit < 0 or digit > 7:
        raise ValueError("Invalid digit. Must be between 0 and 7.")

    permission_map = {
        0: '---',
        1: '--x',
        2: '-w-',
        3: '-wx',
        4: 'r--',
        5: 'r-x',
        6: 'rw-',
        7: 'rwx',
    }
    return permission_map[digit]
def convert_permission(triple):
    """
    Convert a triple of numbers (e.g., 644) into the 'rwx' equivalent (e.g., 'rw-r--r--').

    Args:
        triple (int): A triple of numbers representing permissions (e.g., 644).

    Returns:
        str: The 'rwx' equivalent representation (e.g., 'rw-r--r--').
    """
    if triple < 0 or triple > 777:
        raise ValueError("Invalid permission triple. Must be between 0 and 777.")

    # Convert each digit of the triple to its 'rwx' equivalent
    owner = convert_digit(triple // 100)
    group = convert_digit((triple // 10) % 10)
    others = convert_digit(triple % 10)

    return owner + group + others

class FileSystem:
    current_location = None
    working_directory = None
    def __init__(self):
        db_name = "filesystem.sqlite"
        self.crud = SQLiteCRUD(db_name)
        if FileSystem.current_location == None:
            FileSystem.current_location = "1" #used to check our position inside of functions.
        if FileSystem.working_directory == None:
            FileSystem.working_directory = "1" #where we are.

    '''
    Here is the list of all the table columns we will be using:
        #0     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #1     pid INTEGER NOT NULL, (pid 0 is root and should not be accessible.)
        #2     filename TEXT NOT NULL,
        #3     file_type TEXT NOT NULL,
        #4     file_size INTEGER,
        #5     owner TEXT NOT NULL,
        #6     group_name TEXT NOT NULL,
        #7     permissions TEXT NOT NULL,
        #8     modification_time DATETIME,
        #9     content BLOB
        #10     hidden NUMBER (0 visible, 1 hidden) 
    '''

    def buildDB(self):
        # Define table schema
        table_name = "files"
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "pid INTEGER NOT NULL", "filename TEXT NOT NULL", "file_type TEXT NOT NULL", "file_size INTEGER", "owner TEXT NOT NULL", "group_name TEXT NOT NULL", "permissions TEXT NOT NULL", "modification_time DATETIME", "content BLOB", "hidden NUMBER"]
        # Create table
        self.crud.create_table(table_name, columns)

    def close_connection(self):
        """ Close the database connection
        """
        self.crud.close_connection()

    def pathParser(self, path = None):
        """ Parse the path into a list of directories
        """
        Path_List = []
        if(path == None):
            print("Error: No path given.")
        else:
            Redundant_Path_Removal = FileSystem.getFile(self,ID = FileSystem.working_directory)
            if Redundant_Path_Removal[2] in path and Redundant_Path_Removal[2] != "/":
                path = path.replace(str(Redundant_Path_Removal[2]), "")
            Path_List = path.split("/")
            Path_List = [item.strip() for item in Path_List]
            FileSystem.current_location = FileSystem.working_directory
            try:
                #if the first item in the list is blank, we are starting from the root directory.
                if(Path_List[0] == "" or Path_List == None):
                    Path_List.pop(0)
                elif(Path_List[0] == "~"):
                    FileSystem.current_location = "1"
                    Path_List.pop(0)
                for item in Path_List:
                    # .. means go to parent directory of the current directory we are in while processing the path.
                    if(item == ".."):
                        select_query = f"SELECT * FROM files WHERE id = ?"
                        self.crud.cursor.execute(select_query, (FileSystem.current_location,))
                        rows = self.crud.cursor.fetchall()
                        FileSystem.current_location = rows[0][1]
                    #seemingly meaningless item, but it is used to skip over the "." in the path.
                    elif(item == "."):
                        pass
                    #if the last item is blank, we are ending in a directory.
                    elif(item == "" or item == None):
                        pass
                    else:
                        #start by getting the filename of our current directory.
                        try:
                            select_query = f"SELECT * FROM files WHERE id = ?"
                            self.crud.cursor.execute(select_query, (FileSystem.current_location,))
                            rows = self.crud.cursor.fetchall()
                        except:
                            return []
                        #append the name of the directory we are looking for to the name of the current directory.
                        if(rows[0][2] == '/'):
                            item = rows[0][2] + item
                        else:
                            item = rows[0][2] + "/" + item
                        select_query = f"SELECT * FROM files WHERE pid = ? AND filename = ? AND file_type = ?"
                        self.crud.cursor.execute(select_query, (FileSystem.current_location, item, "Directory"))
                        rows = self.crud.cursor.fetchall()
                        FileSystem.current_location = str(rows[0][0])
                ID = str(FileSystem.current_location)
                FileSystem.current_location = FileSystem.working_directory
                return ID                
            except:
                pass

    def getFileId(self,**kwargs):
        """ Find a file id using pid + name
        """
        try:
            (pid, filename) = (kwargs["pid"], kwargs["filename"])
            if(pid == ""):
                pid = FileSystem.working_directory
            select_query = f"SELECT * FROM files WHERE pid = ? AND filename = ? AND NOT file_type = ?"
            self.crud.cursor.execute(select_query, (pid, filename, "Directory"))
            rows = self.crud.cursor.fetchall()
            if rows != []:
                return rows[0][0]
            else:
                return []
        except sqlite3.Error as e:
            return []
    def getFile(self, ID):
        """ Get the full tuple of a file.
        """
        try:
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (ID,))
            rows = self.crud.cursor.fetchall()
            return rows[0]
        except sqlite3.Error as e:
            print(f"Error reading data from the table: {e}")
            return ()        
    def list(self,**kwargs):
        """ List the files and folders in current directory
        """
        try:
            pid = kwargs["pid"]
            if(pid == ""):
                pid = FileSystem.working_directory
            select_query = f"SELECT * FROM files WHERE pid = ?"
            self.crud.cursor.execute(select_query, (pid,))
            rows = self.crud.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error reading data from the table: {e}")
            return []

    def insert_data(self,data = ()):
        """ Insert data into a table
        """
        try:
            if data != ():
                Temp_data_time = data[-3]
                Temp_data_hidden = data[-1]
                Temp_data_name = data[-9]  
                Temp_data_content = data[-2]
                Temp_data_filesize = 0
                Temp_data_time = str(datetime.datetime.now())
                index = Temp_data_time.find(".")
                if Temp_data_content != None:
                    Temp_data_filesize = len(Temp_data_content)

                Temp_data_time = Temp_data_time[:index]
                if "/" in Temp_data_name and Temp_data_name != "/":
                    Temp_data_name = Temp_data_name.split("/")[-1]
                    if Temp_data_name[0] == ".":
                        Temp_data_hidden = "1"
                    else:
                     Temp_data_hidden = "0"
                else:
                    if Temp_data_name[0] == ".":
                        Temp_data_hidden = "1"
                    else:
                     Temp_data_hidden = "0"
                if len(data) == 10:     
                    data = data[0:1] + (Temp_data_name,) + data[2:3] +(Temp_data_filesize,) + data[4:7] + (Temp_data_time,) + data[8:9] + (Temp_data_hidden,)
                else:
                    data = (Temp_data_name,) + data[1:2] +(Temp_data_filesize,) +data[3:6] + (Temp_data_time,) + data[7:8] + (Temp_data_hidden,)
                    
            if data != () and len(data) == 9:
                data = (None, FileSystem.current_location,) + data
                if(data[3] == "Directory"): #renames the directory we plan to create to be named after the parent directory.
                    select_query = f"SELECT * FROM files WHERE id = ?"
                    self.crud.cursor.execute(select_query, (data[1],))
                    target = self.crud.cursor.fetchall()
                    if(target[0][2] == '/'):
                        stuff = target[0][2] + data[2]
                    else:
                        stuff = target[0][2] + "/" + data[2]
                    data = data[:2] + (stuff,) + data[3:]
                select_query = f"SELECT * FROM files WHERE pid = ? AND filename = ? AND file_type = ?"
                self.crud.cursor.execute(select_query, (FileSystem.working_directory,data[2],data[3]))
                target = self.crud.cursor.fetchall()
                if target == []: #if the file does not exist in the current directory
                    self.crud.insert_data("files", data)
                    self.Recursive_update_directory_filesize(location = FileSystem.working_directory)
                else:
                    print("Error: File already exists.")
            #if the parent directory is included use it.
            elif data != () and len(data) == 10:
                data = (None,) + data
                #need two checks one for directory names and the other for file names.
                #directory names.
                if(data[3] == "Directory"): #renames the directory we plan to create to be named after the parent directory.
                    select_query = f"SELECT * FROM files WHERE id = ?"
                    self.crud.cursor.execute(select_query, (data[1],))
                    target = self.crud.cursor.fetchall()
                    #editing the data tuple to rename the directory to reference it's parent id's name as well.
                    if(target[0][3] != "Directory"):
                        print("Error: Cannot create a directory in a file.")
                        return
                    elif(target[0][2] == '/'):
                        stuff = target[0][2] + data[2]
                    else:
                        stuff = target[0][2] + "/" + data[2]
                    data = data[:2] + (stuff,) + data[3:]
                select_query = f"SELECT * FROM files WHERE pid = ? AND filename = ? AND file_type = ?"
                self.crud.cursor.execute(select_query, (data[1],data[2],data[3]))
                target = self.crud.cursor.fetchall()
                if target == []: #if the file does not exist in the current directory
                    self.crud.insert_data("files", data)
                    self.Recursive_update_directory_filesize(location = data[0])
                else:
                    print("Error: File already exists.")
            else:
                select_query = f"SELECT * FROM files WHERE id = ?"
                self.crud.cursor.execute(select_query, ("1",))
                target = self.crud.cursor.fetchall()
                if target == []:
                    Temp_data_time = str(datetime.datetime.now())
                    index = Temp_data_time.find(".")
                    #removing microsecconds
                    Temp_data_time = Temp_data_time[:index]
                    self.crud.insert_data("files", (None, 0, "/","Directory",0,"root","root","drwxrwxrwx",Temp_data_time,None,0))
                else:
                    print("Error: Home Directory already exists.")
        except sqlite3.Error as e:
            print(f"Error inserting data from the table: {e}")
    """ This is to delete a row (a file or directory) from our database.
        I plan to use ID to delete the row.
    """
    def remove_data(self,ID):
        """ Remove a row from a table
        """
        try:
            self.crud.delete_data("files", "id", str(ID))
        except sqlite3.Error as e:
            #print(f"Error removing data from the table: {e}")
            pass

    def getWorkingDirectory(self):
        """ Return the current working directory
            The id and name of the current working directory
        """
        try:
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (FileSystem.working_directory,))
            capture = self.crud.cursor.fetchall()
            workingdirectory = []
            workingdirectory.append(capture[0][0])
            workingdirectory.append(capture[0][2])
            return workingdirectory
        except sqlite3.Error as e:
            print(f"Error reading data from the table: {e}")
            return []

    def Recursive_update_directory_filesize(self,**kwargs):
        #This method will recursively update the file size of the current directory and all higher level directories.
        try:
            if kwargs["location"] == "":
                FileSystem.current_location = str(FileSystem.working_directory)
            else:
                FileSystem.current_location = str(kwargs["location"])
            select_query = f"SELECT * FROM files WHERE pid = ?"
            self.crud.cursor.execute(select_query, (FileSystem.current_location,))
            capture = self.crud.cursor.fetchall()
            file_size = 0
            #sum up all the file sizes of all files and directories in the current directory.
            #then update the current directory's file size with the new sum.
            if capture != []:
                for row in capture:
                    file_size += row[4]
            self.crud.update_data("files", "file_size", file_size, "id", FileSystem.current_location)
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (FileSystem.current_location,))
            capture = self.crud.cursor.fetchall()
            #if our current directory is not the root directory, we will recursively call this method again.            
            if capture != [] and capture[0][1] != 0:
                #this sets the location to the parent directory.
                FileSystem.current_location = str(capture[0][1])
                self.Recursive_update_directory_filesize(location = FileSystem.current_location)
            else:
                #As we exist we want to return to our original directory.
                FileSystem.current_location = FileSystem.working_directory[:]
        except sqlite3.Error as e:
            print(f"Error adjusting directory size from the table: {e}")
    #this will recursively update the directory name of the passed directory and all lower level directories.
    def Recursive_update_directory_filename(self,**kwargs):
        try:
            name = kwargs["name"]
            old_base = kwargs["old_base"]
            new_base = kwargs["new_base"]
            #fetching the id of the directory we are changing the name of.
            select_query = f"SELECT * FROM files WHERE filename = ? and file_type = ?"
            self.crud.cursor.execute(select_query, (name,"Directory"))
            capture = self.crud.cursor.fetchall()
            #if the directory exists, we can change the name.
            if capture != []:
                #now we need to keep track of the old name for the recursion. This is name
                #we need to replace the portion of the old name with the name name.
                name_base = capture[0][2].replace(old_base, new_base)
#                print(name_base)
                self.crud.update_data("files", "filename", name_base, "id", capture[0][0])
                #moved name to old_base for the recursion
                old_base = name[:]
                #now we need to check all the directories beneath this directory to adjust their names as well.
                select_query = f"SELECT * FROM files WHERE pid = ? and file_type = ?"
                self.crud.cursor.execute(select_query, (capture[0][0],"Directory"))
                capture = self.crud.cursor.fetchall()
                if capture != []:
                    for directory in capture:
                        name = directory[2][:] #name of the directory we are changing the name of.
                        self.Recursive_update_directory_filename(name=name, old_base=old_base, new_base = name_base)
                    else:
                        #no targets, end recursion
                        pass
            else:
                print("Error: Directory does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting directory name from the table: {e}")
    def getContent(self,ID):
        """ Get the content of a file
        """
        try:
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (ID,))
            capture = self.crud.cursor.fetchall()
            return capture[0][9]
        except sqlite3.Error as e:
            print(f"Error reading data from the table: {e}")
            return []
    def setWorkingDirectory(self,ID):
        FileSystem.working_directory = str(ID)

#This block of methods will be all the update methods for the filesystem
    def chmod(self,**kwargs):
        """ Change the permissions of a file
        """
        try:
            id = kwargs["id"]
            #string of 3 numbers
            perm = kwargs["permission"]
            new_perm = ""
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #if the file exists, we can change the permissions.
            if capture != []:
                #check to see if it is a directory
                if capture[0][3] == "Directory":
                    new_perm = "d"
                    try:
                        if type(int(perm)) == int:
                            concat = convert_permission(int(perm))
                            new_perm = new_perm + concat
                    except:
                        new_perm = new_perm + perm
                else:
                    new_perm = "-"
                    try:
                        if type(int(perm)) == int:
                            concat = convert_permission(int(perm))
                            new_perm = new_perm + concat
                    except:
                        new_perm = new_perm + perm
            self.crud.update_data("files", "permissions", new_perm, "id", id)
        except sqlite3.Error as e:
            print(f"Error adjusting file permissions from the table: {e}")
    def chfilesize(self,**kwargs):
        """ Change the size of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                #get the id for the file/directory if it exists
                condition_value = capture[0][0]
                if capture[0][3] != "Directory":
                    self.crud.update_data("files", "file_size", new_value, "id", condition_value)
                else:
                    print("Error: Cannot change the size of a directory.")
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting file size from the table: {e}")
    def chown(self,**kwargs):
        """ Change the owner of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                self.crud.update_data("files", "owner", new_value, "id", id)
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting owner from the table: {e}")
    def chgrp(self,**kwargs):
        """ Change the group of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                self.crud.update_data("files", "group_name", new_value, "id", id)
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting group from the table: {e}")
    def chname(self,**kwargs):
        """ Change the name of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            target_file = self.crud.cursor.fetchall()
            #make sure the file exists
            if target_file != []:
                #get the id for the directory of the file if it exists
                pid = target_file[0][1]
                #if we are changing the name of a directory we need to concatenate the name of the parent directory to the name of the directory we are changing.
                #before we name check to make sure the directory we are changing to does not already exist.
                if target_file[0][3] == "Directory":
                    if str(self.crud.get_data("files", "filename", "id", pid)) != "/":
                        new_value = str(self.crud.get_data("files", "filename", "id", pid)) + "/" + new_value
                    else:
                        new_value = str(self.crud.get_data("files", "filename", "id", pid)) + new_value
                    #now we check for any directories beneath this directory to adjust their names as well.
                #check the current directory for a file with the same name.
                select_query = f"SELECT * FROM files WHERE filename = ? AND pid = ?"
                self.crud.cursor.execute(select_query, (new_value,pid))
                capture = self.crud.cursor.fetchall()
                #if no file with the same name exists, we can change the name of the file.
                if capture == []:
                    Temp_Tuple = self.getFile(id)
                    if target_file[0][3] == "Directory":
                        #get the last part of the directory name and do not care about the root..
                        if "/" in Temp_Tuple[2] and Temp_Tuple[2] != "/" :
                            Temp_Name = Temp_Tuple[2].split("/")[-1]
                            if Temp_Name[0] == ".":
                                self.chhidden(id = id, new_value = "1")
                            else:
                                self.chhidden(id = id, new_value = "0")
                        else:
                            if Temp_Tuple[2][0] == ".":
                                self.chhidden(id = id, new_value = "1")
                            else:
                                self.chhidden(id = id, new_value = "0")

                        self.Recursive_update_directory_filename(name=target_file[0][2], old_base=target_file[0][2], new_base = new_value)
                    else:
                        #get the last part of the directory name and do not care about the root..
                        if "/" in Temp_Tuple[2] and Temp_Tuple[2] != "/" :
                            Temp_Name = Temp_Tuple[2].split("/")[-1]
                            if Temp_Name[0] == ".":
                                self.chhidden(id = id, new_value = "1")
                            else:
                                self.chhidden(id = id, new_value = "0")
                        else:
                            if Temp_Tuple[2][0] == ".":
                                self.chhidden(id = id, new_value = "1")
                            else:
                                self.chhidden(id = id, new_value = "0")
                        self.crud.update_data("files", "filename", new_value, "id", id)
                else:
                    print("Error: File with that name already exists.")
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting file name from the table: {e}")
    def chdir(self,**kwargs):
        """ Change the current working directory
        This method is tricky because we need to check for two directions.
        If we are going up a directory, we need to check if the current directory is the root directory.
        and if we are going down a directory, we need to check if the directory we are going to exists.
        Up does not move by name but rather by ".." which will tell us to move to the parent directy. pid
        Down moves by name, but only the last part of the name after the last "/".
        """
        try:
            ID = kwargs["ID"]
            select_query = f"SELECT * FROM files WHERE id = ? AND file_type = ?"
            self.crud.cursor.execute(select_query, (ID,"Directory"))
            capture = self.crud.cursor.fetchall()
            if capture != []:
                FileSystem.working_directory = str(ID[:])
            else:
                print("Error: Directory does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting directory from the table: {e}")

    def chcontent(self,**kwargs):
        """ Change the content of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                if capture[0][3] != "Directory":
                    self.crud.update_data("files", "content", new_value, "id", id)
                    #get the file tuple and run the recursive directory update on the pid of the file.
                    Temp_File = self.getFile(id)
                    self.chfilesize(id = id, new_value = len(Temp_File[9]))
                    self.Recursive_update_directory_filesize(location = int(Temp_File[1]))
                else:
                    print("Error: Cannot change the content of a directory.")
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting content from the table: {e}")

    def chmodtime(self,**kwargs):
        """ Change the modification time of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                self.crud.update_data("files", "modification_time", new_value, "id", id)
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting mod_time from the table: {e}")
        
    def chhidden(self,**kwargs):
        """ Change the hidden status of a file/directory
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                self.crud.update_data("files", "hidden", new_value, "id", id)
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting hidden from the table: {e}")
            
    def chtype(self,**kwargs):
        """ Change the type of a file/directory.
            A file cannot become a directory and vice versa.
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a file and not a directory.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            capture = self.crud.cursor.fetchall()
            #make sure the file exists
            if capture != []:
                #get the filetype for the file/directory if it exists
                condition_value = capture[0][3]
                if condition_value == "Directory":
                    print("Error: Cannot change the type of a directory.")
                elif condition_value != "Directory" and new_value == "Directory":
                    print("Error: Cannot change the type of a file to directory.")
                else:
                    self.crud.update_data("files", "file_type", new_value, "id", id)
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting mod_time from the table: {e}")
    def chpid(self,**kwargs):
        """ Change the parent id of a file
        """
        try:
            id = kwargs["id"]
            new_value = kwargs["new_value"]
            #make sure the target is a row in the database.
            select_query = f"SELECT * FROM files WHERE id = ?"
            self.crud.cursor.execute(select_query, (id,))
            target_file = self.crud.cursor.fetchall()
            if target_file != []:
                select_query = f"SELECT * FROM files WHERE id = ?"
                self.crud.cursor.execute(select_query, (new_value,))
                target_pid = self.crud.cursor.fetchall()
                #if the new pid is a directory and it exists.
                if target_pid != [] and target_pid[0][3] == "Directory" and target_pid[0][0] != 1:
                    #now to make sure we are not creating a naming conflict.
                    #directory here gets really complicated and annoying.
                    if target_file[0][3] == "Directory":
                        #this is the last part of the directory name.
                        place_holder_key_identifier = target_file[0][2].split("/")[-1]
                        file_name = target_pid[0][2] + "/" + place_holder_key_identifier
                    else:
                        file_name = target_file[0][2]

                    self.query = f"SELECT * FROM files WHERE pid = ? AND filename = ? AND file_type = ?"
                    self.crud.cursor.execute(self.query, (new_value,file_name,target_file[0][3]))
                    capture = self.crud.cursor.fetchall()
                    #if we are changing the PID of a directory we need to update the name as well.
                    if capture == []:
                        if target_file[0][3] == "Directory":
                            self.crud.update_data("files", "pid", new_value, "id", id)
                            self.Recursive_update_directory_filename(name=target_file[0][2], old_base=target_file[0][2], new_base = file_name)
                        else:
                            self.crud.update_data("files", "pid", new_value, "id", id)
                    else:
                        print("Error: File type with that name already exists.")
                elif target_pid[0][0] == 1:
                    print("Error: cannot rename root.")
                else:
                    print("Error: Cannot change the parent id to a file.")
            else:
                print("Error: File does not exist.")
        except sqlite3.Error as e:
            print(f"Error adjusting PID from the table: {e}")



# Example usage:
if __name__ == "__main__":
    FileSYS = FileSystem()
    FileSYS.buildDB() 

    FileSYS.insert_data()
    FileSYS.insert_data(("home", "Directory", 0, "root", "root", "drwxrwxrwx", "2021-12-01 00:00:00", None, "0"))
    FileSYS.insert_data(("1", "bhist", "file", 0, "root", "root", "-rwxrwxrwx", "2023-12-03 00:00:00", "", "0"))
    # FileSYS.insert_data(("10", "Redirect", "file", 0, "root", "root", "-rwxrwxrwx", "2023-12-03 00:00:00", "", "0"))
    FileSYS.insert_data(("1", "ibacon",".txt",25,"root","root","-rwxrwxrwx","2023-12-03 00:00:00","Bacon ipsum dolor amet swine jowl pastrami ribeye prosciutto cow kevin hamburger corned beef pork chop. \nSwine turducken kevin, bresaola flank ribeye fatback meatloaf ham hamburger tail alcatra. \nPicanha short loin tongue meatball. \nSalami shank tri-tip pork chop filet mignon. \nCapicola buffalo pig ball tip, biltong turkey doner kielbasa pork loin fatback prosciutto shankle. \nTri-tip short loin picanha chicken swine flank. \nAlcatra kevin tail ball tip beef fatback bacon andouille.\nVenison shoulder kielbasa meatloaf bacon pork loin pancetta short ribs strip steak salami meatball sirloin pork. \nCapicola ham hock filet mignon venison sausage short ribs. \nSausage biltong t-bone porchetta prosciutto filet mignon, pig pork belly swine burgdoggen beef salami pork loin pork chop. \nSalami bresaola sirloin pastrami brisket kielbasa.\nApples Meatball biltong rump frankfurter chicken pork belly. \nApples Landjaeger capicola kevin filet mignon, shoulder andouille drumstick shankle. \nApples Fatback chicken pork swine doner meatloaf turkey. \nAlcatra ham hock burgdoggen drumstick pastrami, porchetta kielbasa corned beef fatback venison jowl. \nCorned beef boudin doner shank, biltong burgdoggen turkey jowl kevin rump pancetta short ribs cupim tri-tip. Beef ribs meatball jowl salami filet mignon venison. \nRump drumstick cow kielbasa turducken boudin prosciutto.\nBeef ribs tongue kielbasa fatback jerky, turkey andouille corned beef tail pig ribeye meatball leberkas jowl. \nBoudin rump tenderloin, meatball beef ribs pork pastrami. \nBall tip beef cupim, shank ribeye chicken bacon meatloaf fatback pork loin tenderloin filet mignon landjaeger. \nCorned beef salami strip steak boudin venison cow ham biltong frankfurter capicola. \nKielbasa ribeye andouille buffalo alcatra, beef rump ham hock leberkas hamburger tri-tip porchetta venison. Beef ribs tenderloin cupim burgdoggen.\nMeatloaf alcatra shank short loin, doner brisket pig rump. Tail tongue jerky salami short ribs. \nHamburger beef landjaeger, sausage prosciutto strip steak jowl ham hock swine. \nBoudin sirloin pork chop, t-bone doner ham ground round turkey cow landjaeger drumstick. \nTail flank turkey ham hock shankle.\nDoes your lorem ipsum text long for something a little meatier? \nGive our generator a try… it’s tasty!","0"))
    FileSYS.insert_data(("1", "ilorem",".txt",25,"root","root","-rwxrwxrwx","2023-12-03 00:00:00","Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et massa dolor. \nUnc mattis dolor non felis aliquam posuere. \nNunc pulvinar, ligula eget molestie auctor, arcu ligula lobortis velit. \nUnt scelerisque mi mauris vehicula tellus. Donec malesuada ipsum odio, id viverra libero aliquam id. \nFusce sodales nisl velit, nec faucibus sapien blandit eget. \nNulla sit amet mi at nunc placerat ornare. \nEtiam blandit purus nec massa scelerisque, id luctus tellus lacinia. \nProin feugiat enim vitae dui sollicitudin, sit amet scelerisque enim vehicula. \nNam ipsum libero, tempor vitae consectetur quis, auctor in orci. Duis id pulvinar lorem. \nProin et feugiat augue, vel scelerisque mauris. \nUt condimentum orci nec diam rutrum, a mollis lectus luctus. \nApples Nunc sit amet est eu ipsum blandit tempor vel eu libero. \nApples Curabitur euismod elit vel consectetur accumsan.\nSuspendisse eget orci euismod, tempus tellus ut, facilisis velit. \nNunc vel luctus diam, at imperdiet magna. \nApples Aliquam ac auctor metus. \nIn commodo nisi id leo venenatis, vitae lobortis neque fermentum. \nApples Cras auctor, mi in lobortis tincidunt, felis nulla mollis nisi, sed faucibus ligula metus ac libero. \nFusce vehicula quis sapien quis tempor. Sed ac ullamcorper ex. \nMorbi pellentesque diam vehicula, viverra mi non, egestas nulla. \nPraesent non quam erat. Integer ultrices mollis diam in consectetur. \nAenean ac metus mi. Aenean commodo commodo diam, quis mollis dui finibus et. \nEtiam eleifend sem ut purus fringilla maximus. \nMaecenas leo metus, sollicitudin quis orci eget, placerat interdum urna.\nNam eget odio vitae odio ultrices maximus vel in risus. \nOrci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec massa nibh, volutpat sed facilisis quis, pulvinar eu nibh. \nInteger facilisis urna vitae lectus vehicula, eu suscipit nibh condimentum. \nFusce laoreet tortor feugiat purus dictum ornare. \nMaecenas non erat a nisi condimentum imperdiet. \nPellentesque iaculis eu diam eget efficitur. Vivamus malesuada, nisl quis fringilla vestibulum, lectus orci dictum massa, vel pellentesque nunc nisl ac est. \nVivamus dictum dui eu hendrerit lobortis. Mauris sed lorem non nibh pretium ultricies. \nAliquam eget neque vitae urna malesuada aliquet nec sit amet nisi. Duis id lacinia purus.","0"))

    FileSYS.insert_data(("2","numbers", ".txt", 0, "root", "root", "-rwxrwxrwx", "2021-04-03 00:00:00", "1. \n2. \n3. \n4. \n5. \n6. \n7. \n8. \n9. \n10. \n11. \n12. \n13. \n14. \n15. \n16. \n17. \n18. \n19. \n20. \n21. \n22. \n23. \n24. \n25. \n26. \n27. \n28. \n29. \n30.", "0"))
    FileSYS.insert_data(("2","apples",".txt",25,"root","root","-rwxrwxrwx","2023-02-12 00:00:00","Don't mess with them Apples. \nApples are great. \nCuz an Apple a day keeps the doctor away. \nBetter than Bananas are them Apples. \nActually no Bananas are better.","0"))
    FileSYS.insert_data(("2","oranges",".txt",25,"root","root","-rwxrwxrwx","2023-05-02 00:00:00","Oranges are a fruit. \nSunshine in a peel \nCitrus love in every bite.","0"))
    FileSYS.insert_data(("2","bananas",".txt",25,"root","root","-rwxrwxrwx","2023-06-15 00:00:00","Bananas are also a fruit. \nJust hanging out, like a banana. \nKeep calm and eat a banana.","0"))

    FileSYS.crud.read_data("files")

    FileSYS.crud.close_connection()