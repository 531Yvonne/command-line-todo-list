# This Application is a Minimalist Command Line To-Do List
Fancy task managers with slick user interfaces are slow and cumbersome. With the power of command line at disposal, I'd like to access all tasks without tedious pointing and clicking.

This program is an object oriented task manager application that will allow user to enter tasks, save them to a file, and retrieve them... all without moving your hands from the keyboard.

[![Watch the video](https://img.youtube.com/vi/Bf1JCaIo9FM/maxresdefault.jpg)](https://youtu.be/Bf1JCaIo9FM)

## Usage
The user can run the program completely from the command line
passing in commands and arguments that will alter the behavior of the program.
The commands are --help, --add, --delete, --list, --report, --query, and --done. 

### `python todo.py --help`
Show the commands manual


### `python todo.py --add "Grocery run" --due 3/20/2018 --priority 3`
Add a new task with task description, optional due date and priority

### `python todo.py --list`
Display a list of the not completed tasks sorted by the due date.
If tasks have the same due date, sort by decreasing priority
(1 is the highest priority).
If tasks have no due date, then sort by decreasing priority.

### `python todo.py --query eggs`
Search for incomplete tasks that match a certain term (or multiple terms).

### `python todo.py --done 1`
Complete a task by passing the done argument and the unique identifier.

### `python todo.py --delete 3`
Delete a task by passing the --delete command and the unique identifier.

### `python todo.py --report`
List all tasks, including both completed and incomplete tasks,
It follows the same reporting order as the --list command.


## Implementation:
Task class and Tasks class are created for data representation
Data are serialized to disk using Python pickle module

## Execution:
To make this task manager program an executable program in order to 
run from any location on your computer:

Place a copy of it in a place where $PATH is looking for executable files:
for my own case: /usr/local/bin:

Add a shebang line to the top of the code:
  #!/usr/bin/env python

Mark the script as executable:
  chmod +x todo.py

.todo.pickle file will be saved in user's home directory.
