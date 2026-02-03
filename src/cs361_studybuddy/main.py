from ssl import Options
from loguru import logger
#from art import *
from rich import print
from rich.prompt import Prompt
#from typing import list
#from rich import print
from rich.table import Table

def download_task_list(task_list: list[str]) -> list[int, str]:
    #find textfile in folder csv or text??
    #if not found, create file
    #read from file and add to list
    #return the list
    # if()
    try:
        with open("task.txt", "r") as file:
            line = file.readline()
            while line:
                task_list.append(line)
                line = file.readline()
    except FileNotFoundError:
        return
    # return 0

def upload_task_list(task_list: list[str]) -> list[int, str]:
    #find textfile in folder csv or text??
    #if not found, create file
    #read from file and add to list
    #return the liust
    with open("task.txt", "w") as file:
        for line in task_list:
            file.write(line)
    return 0

def print_task_list(task_list: list[str]) -> None:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()
    for idx, task in enumerate(task_list):
        grid.add_row(f"{idx}", f"{task}")

    print(grid)
    #for each print??
    return;

def add_task(task_list: list[str]) -> None:
    #print the prompt for add a task
    #accept user input
    # while loop 
    #ask if they want to edit
    #call edit if yes
    #once out of loop, add task to list
    # use len to find end of list to find new num for task
    task: str = input("Adding a task! Type contents here:")
    task_list.append(task)
    print(f" Task {task} added!")

    return;

def edit_task(task_list: list[str]) -> None:
    #ask for new string
    #get new string
    #return it
    idx = input("Which task do you want to edit?")
    old_task = task_list[idx]
    print(f"old task: {old_task}")
    task: str = input("new task: ")
    task_list[idx] = task
    #return " "

def delete_task(task_list: list[str]) -> None:
    idx = input("Which task would you like to delete?")
    print(f"Are you sure you want to delete task {task_list[idx]}?\n This action is irreversible!")
    conf = input("Type Y for yes, N for no:")
    match conf:
        case "Y":
            task_list.pop(idx)
        case "N":
            return
    #ask are you sure??
    #if no then return
    #if yes then delete from list
    # print deleted
    # return;


def render_help_page() -> None:
    #figure out how to use rich to make this look nice!
    #header home page
    #instructions
    #header task page
    #instructions
    print("I Need Help!\nWelcome to Study Buddy!\nOn the home page:\nTo view your to do list, type v\nOnce you are viewing your to do list, type a to add to your list, or d to delete from your list\nTo add to your to do list, type a\nQuestions? Contact help@studybuddy.com!")
    return;

#use rich prompting!!!
def open_task_page(task_list: list[str]) -> None:
    while True:
        print(task_list)
        print("Want to work on your list? a - add a task\nd - delete a task\ne - edit a task\nexit - exit to do list")
        option = input("enter command here:")
        match option:
            case "a":
                add_task(task_list)
            case "d":
                delete_task(task_list)
            case "e":
                edit_task(task_list)
            case "exit":
                print("Exiting Task List!")
                break;
    #while loop
    #print list
    #print options list
    



def main() -> None:
    logger.info("template-project")
    print("welcome to study buddy")

    task_list: list[str] = []
    download_task_list(task_list)
    print("A study tool to help you keep track of your tasks so you can have a more efficient study session!")
    while True:
        print("Type the command and press enter to navigate to the page!")
        print("v - view to do list\nh - help page\na - add a task to list\nexit - exit studdy buddy")
        option: str = input("enter command here:")
        match (option):
            case "v":
                open_task_page(task_list)
            case "h":
                render_help_page()
            case "a":
                add_task(task_list)
            case "exit":
                upload_task_list(task_list)
                break
    #read from text file and put all the stuff in the list
    #print all Options
    #while loop
    #case statement for input
    #default is try again/not a vlid option
    #pick help -> help func that displays options and text
    #pick to do -> to do func that calls print list and displays options
        #while loop with options
    #pick exit-> write the todo list to the text file and quit
    #list are pass by ref!




    


if __name__ == "__main__":
    main()