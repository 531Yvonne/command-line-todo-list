# Command Line Task Manager
#
# Written by Yves Yang

import time
from datetime import datetime
import pickle
import argparse
import tabulate
import re
import pendulum


class Task:
    '''Representation of one task

    Attributes:
        - created - Date
        - created_formatted - String of creation date in a specific format
        - completed - Date
        - name - String
        - unique_id - Number
        - priority - Int value of 1, 2, or 3; 1 is default, 3: highest priority
        - due_date - Date, this is optional
    '''

    def __init__(self, name, unique_id=0, priority=1,
                 due_date=None, completed=None):
        # Attribute to store creation time in float format
        self.created = time.time()
        # Attribute to store creation time in required listing/reporting format
        self.created_formatted = time.ctime(self.created)[:-5] + " CST "\
            + time.ctime(self.created)[-4:]
        self.completed = completed
        self.name = name
        self.unique_id = unique_id
        self.priority = priority
        self.due_date = due_date


class Tasks:
    '''A list of "Task" objects.'''

    def __init__(self):
        '''Read pickled tasks file into a list'''
        # List of Task objects
        self.tasks = []
        # Task the max task id for future new task unique_id assignment
        self.max_id = 0

        # When no pickled file saved during first run, pickle a file first
        try:
            with open(".todo.pickle", "rb") as f:
                items = pickle.load(f)
        except:
            self.pickle_tasks()
        # Store unpickled tasks to a list
        else:
            for i in items:
                self.tasks.append(i)
        # Track the current max task id for any new unique_id assignment
        finally:
            if self.tasks != []:
                self.max_id = max([item.unique_id for item in self.tasks])

    def pickle_tasks(self):
        '''Pickle your task list to a file'''
        with open(".todo.pickle", "wb") as f:
            pickle.dump(self.tasks, f)

    def add(self, name, priority=1, due_date=None):
        '''Add new task to tasks'''
        new_task = Task(name, self.max_id + 1, priority, due_date)
        self.tasks.append(new_task)
        print("Create task", new_task.unique_id)

    def get_age(self, item):
        '''Helper function to get the age of a task'''
        delta = datetime.fromtimestamp(
            time.time()) - datetime.fromtimestamp(item.created)
        age = str(delta.days) + "d"
        return age

    def get_completion_date(self, item):
        '''
        Helper function to get the string for completion date
        in listing/reporting format
        '''
        if item.completed is None:
            due = "-"
        else:
            due = item.completed
        return due

    def list_sorting(self, data_wo_due_date, data_w_due_date):
        '''
        Sort the tasks by due date (closest first),
        then by priority(highest first)
        '''
        # For tasks without due date, sort by priority only
        data_wo_due_date = sorted(
            data_wo_due_date, key=lambda data_wo_due_date: -data_wo_due_date[3])
        # For tasks with due date, sort by due date (closest to furthest)
        # then by priority
        data_w_due_date = sorted(data_w_due_date, key=lambda data_w_due_date: (
            data_w_due_date[2], -data_w_due_date[3]))
        for task in data_w_due_date:
            # Update original datetime(used for sorting)
            # to proper MM/DD/YYYY view format
            task[2] = task[2].strftime('%m/%d/%Y')
        # Attach two lists together
        data = data_w_due_date + data_wo_due_date
        return data

    def list(self):
        '''List all incomplete tasks'''

        # Here I store the tasks into two list, in order to rank
        # all no due-date tasks below tasks with due date
        # Split and sort separately then attach two lists together
        data_w_due_date = []
        data_wo_due_date = []
        for item in self.tasks:
            if item.completed is None:
                age = self.get_age(item)
                if item.due_date is None:
                    data_wo_due_date.append(
                        [item.unique_id, age, "-", item.priority, item.name])
                else:
                    data_w_due_date.append(
                        [item.unique_id, age, item.due_date,
                         item.priority, item.name])
        data = self.list_sorting(data_wo_due_date, data_w_due_date)
        print(tabulate.tabulate(data, headers=[
              "ID", "Age", "Due Date", "Priority", "Task"]))

    def report(self):
        '''Report all tasks'''
        data_w_due_date = []
        data_wo_due_date = []
        for item in self.tasks:
            age = self.get_age(item)
            complete = self.get_completion_date(item)
            if item.due_date is None:
                data_wo_due_date.append(
                    [item.unique_id, age, "-", item.priority, item.name,
                     item.created_formatted, complete])
            else:
                data_w_due_date.append([item.unique_id, age, item.due_date,
                                       item.priority, item.name,
                                       item.created_formatted, complete])
        data = self.list_sorting(data_wo_due_date, data_w_due_date)
        print(tabulate.tabulate(data, headers=[
              "ID", "Age", "Due Date", "Priority", "Task", "Created",
              "Completed"]))

    def done(self, task_id):
        '''Mark task with given id as completed and store the complete time'''
        current_ids = [i.unique_id for i in self.tasks]
        # Check whether the input is a valid task
        if task_id not in current_ids:
            print(
                f"Can't Complete! Task {task_id} is not in your to-do list!")
            exit()
        complete_time = time.time()
        print("Completed task", task_id)
        for item in self.tasks:
            if item.unique_id == task_id:
                item.completed = time.ctime(complete_time)[
                    :-5] + " CST "+time.ctime(complete_time)[-4:]
                return

    def delete(self, task_id):
        '''Delete task with given id from the todo list'''
        current_ids = [i.unique_id for i in self.tasks]
        # Check whether the input is a valid task
        if task_id not in current_ids:
            print(
                f"Can't Delete! Task {task_id} is not in your to-do list!")
            exit()
        for item in self.tasks:
            if item.unique_id == task_id:
                print("Deleted task", task_id)
                self.tasks.remove(item)
                return

    def query(self, keyword):
        '''list out tasks containing keyword(s) in task name'''
        data_w_due_date = []
        data_wo_due_date = []
        for item in self.tasks:
            if item.completed is None:
                for word in keyword:
                    if word.upper() in item.name.upper():
                        age = self.get_age(item)
                        if item.due_date is None:
                            data_wo_due_date.append(
                                [item.unique_id, age, "-", item.priority,
                                 item.name])
                        else:
                            data_w_due_date.append(
                                [item.unique_id, age, item.due_date,
                                 item.priority, item.name])
        data = self.list_sorting(data_wo_due_date, data_w_due_date)
        print(tabulate.tabulate(data, headers=[
              "ID", "Age", "Due Date", "Priority", "Task"]))


def pendulum_finder(x):
    ''' This function return the date for specific weekday named input'''
    x = x.lower()
    if x in ["monday", "mon", "next monday"]:
        # Get date string for next Monday
        x = pendulum.now().next(pendulum.MONDAY)
    elif x in ["tuesday", "tues", "tue", "next tuesday"]:
        x = pendulum.now().next(pendulum.TUESDAY)
    elif x in ["wednesday", "next wednesday", "wed"]:
        x = pendulum.now().next(pendulum.WEDNESDAY)
    elif x in ["thursday", "next thursday", "thu", "thur"]:
        x = pendulum.now().next(pendulum.THURSDAY)
    elif x in ["friday", "next friday", "fri"]:
        x = pendulum.now().next(pendulum.FRIDAY)
    elif x in ["saturday", "next saturday", "sat"]:
        x = pendulum.now().next(pendulum.SATURDAY)
    elif x in ["sunday", "next sunday", "sun"]:
        x = pendulum.now().next(pendulum.SUNDAY)
    else:
        return False
    return x.strftime('%m/%d/%Y')


def main():
    parser = argparse.ArgumentParser(description='Update your ToDo list.')
    # Add an argument
    parser.add_argument('--add', type=str, required=False,
                        help='a task string to add to your list, enclosed\
                            in quotes if there are mulitple words.')
    parser.add_argument('--due', type=str, required=False,
                        help='due date in MM/DD/YYYY format')
    parser.add_argument('--priority', type=int, required=False, default=1,
                        help="priority of task; default is 1, Highest is 3")
    parser.add_argument('--query', type=str, required=False, nargs="+",
                        help="list out tasks containing keyword(s) in name")
    parser.add_argument('--list', action='store_true', required=False,
                        help="list all tasks that have not been completed")
    parser.add_argument('--report', action='store_true',
                        required=False, help="list all tasks")
    parser.add_argument('--delete', type=int, required=False,
                        help="delete a task with given id ")
    parser.add_argument('--done', type=int, required=False,
                        help="mark a task with given id as completed")
    # Parse the argument
    args = parser.parse_args()
    tasks = Tasks()

    # Launch Add Operation
    if args.add:
        # Per Canvas example: return error for any task name with only numbers
        if re.match(r'^[ 0-9]+$', args.add):
            print('There was an error in creating your task.\
                  (Task Name shouldn\'t be only numbers) Run "todo -h" for\
                  usage instructions.')
            exit()
        if args.due:
            # due date input names a specific weekday
            if pendulum_finder(args.due) is not False:
                args.due = pendulum_finder(args.due)
            # due date input not in any strings above,
            # check whether it's a valid MM/DD/YYYY
            elif re.match(r'^(0?[1-9]|1[12])[/](0?[1-9]|[12][0-9]|3[01])[/](\d{4})$', args.due) is None:
                print(
                    'There was an error in due date format.\
                        (Should be MM/DD/YYYY) Run "todo -h"\
                            for usage instructions.')
                exit()
            # Convert the date string to a datetime data
            args.due = datetime.strptime(args.due, "%m/%d/%Y")
        if args.priority:
            if args.priority not in [1, 2, 3]:
                print('There was an error in priority. (Should be 1, 2, 3. And\
                      3 is the highest priority) Run "todo -h" for usage\
                      instructions.')
                exit()
        tasks.add(args.add, args.priority, args.due)

    # Launch Report Operation
    if args.report:
        tasks.report()

    # Launch List Operation
    if args.list:
        tasks.list()

    # Launch Query Operation
    if args.query:
        tasks.query(args.query)

    # Launch Done Operation
    if args.done:
        tasks.done(args.done)

    # Launch Delete Operation
    if args.delete:
        tasks.delete(args.delete)

    # Pickle the file after each run of operation
    tasks.pickle_tasks()


if __name__ == "__main__":
    main()
