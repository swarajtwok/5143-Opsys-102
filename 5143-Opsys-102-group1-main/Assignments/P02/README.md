## Shell implementation using Virtual Filesystem

### Group Members
| Member | Github Repo |
| ------ | ----------- |
| Chintan Mehta | **[chill-chin](https://github.com/chill-chin)** |
| Michael Ellerkamp | **[ILDivino](https://github.com/ILDivino/5143-Opsys-102)** |
| Swaraj Chirumamilla | **[swarajtwok](https://github.com/swarajtwok/5143-Opsys-102)** |

### Files
|   #   | Directory                                   | Description                               |
| :---: | -------------------------------------- | ---------------------------------------------------- |
|   1   | [cmd_pkg_use](https://github.com/chill-chin/5143-Opsys-102-group1/tree/main/Assignments/P02/cmd_pkg_use) | [Folder with all the code for P02](https://github.com/chill-chin/5143-Opsys-102-group1/tree/main/Assignments/P02/cmd_pkg_use) |

### Overview:
* This is a project written in python that implements a basic shell. The project involves using a virtual filesystem implemented in backend, and the shell commands are implemented on top of this filesystem.


### Instructions:
* Download [cmd_pkg_use](https://github.com/chill-chin/5143-Opsys-102-group1/tree/main/Assignments/P02/cmd_pkg_use) from P02 Repository.
* Run the command: **python3 -m pip install rich**
* Run [fileSystem.py](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/fileSystem.py), in order to create sqlite Table.
* Run [shell_loop.py](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/shell_loop.py), in order to implement the shell.
* Implement the **commands** described below.

### Commands:
| Command | Description | Usage | Authors |
| ------ | ----------- | -------- | ---- |
| [ls](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdLs.py) | Lists all the files and a directories in the current directory  | "ls -lah", "ls -l" | Chintan, Michael |
| [mkdir](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdMkdir.py) | Creates a directory or a subdirectory | "mkdir dirname" |Michael |
| [cd](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdCd.py) | Changes the current working directory | "cd directory", "cd ..", "cd ~" | Michael |
| [pwd](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdPwd.py) | Prints full path of the current directory | "pwd" | Chintan, Michael |
| [mv](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdMv.py) | Move or rename files | "mv filename dirname" |  Michael, Swaraj |
| [cp](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdCp.py) | Copies files from one location to another | cp file1 file2 | Michael, Swaraj |
| [rm](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdRm.py) | Removes a file or directory | "rm filename", "rm -rf dirname" | Michael, Swaraj |
| [cat](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdCat.py) | Concatenates files and prints them to the standard output | cat file1 file2 | Chintan, Michael |
| [less](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdLess.py) | Shows file's contents one page at a time | "less filename" | Michael |
| [head](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdHead.py) | Prints first few lines of a file | "head -n 3 filename" | Chintan, Michael |
| [tail](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdTail.py) | Prints last few lines of a file | "tail -n 3 filename" | Chintan, Michael |
| [grep](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdGrep.py) | Searches in files for matching string and returns to output | grep "keyword" filename | Michael |
| [wc](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdWc.py) | Prints the number of lines, words or characters in a file | "wc -lw filename" | Chintan, Swaraj |
| [history](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdHistory.py) | Prints a numbered list of all the previous user shell commands | "history" | Michael |
| [chmod](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdChmod.py) | Changes the permissions of files/directories | "chmod 000 filename" | Chintan, Michael |
| [sort](https://github.com/chill-chin/5143-Opsys-102-group1/blob/main/Assignments/P02/cmd_pkg_use/cmd_pkg/cmdSort.py) | Alphabetically sorts the lines of a file | "sort filename", "sort -r filename" | Michael |

### References:

* **ChatGPT:** Used for creating **comment blocks** and **debugging** the code.
 
