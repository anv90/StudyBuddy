from rich.box import SIMPLE_HEAVY
#from ssl import Options
from loguru import logger
from rich import print
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.console import Console
import time
console = Console()

def download_task_list(task_list: list[str]) -> list[str]:
    #find textfile in folder csv or text??
    #if not found, create file
    #read from file and add to list
    #return the list
    # if()
    try:
        with open("src/cs361_studybuddy/task.txt", "r") as file:
            line = file.readline()
            while line:
                task_list.append(line)
                line = file.readline()
    except FileNotFoundError:
        logger.error("file not found")
        return task_list
    else:
        logger.info("file found")
        return task_list

def upload_task_list(task_list: list[str]):
    if(len(task_list) > 0):
        with open("src/cs361_studybuddy/task.txt", "w") as file:
            for line in task_list:
                file.write(f"{line}\n")
    else:
        with open("src/cs361_studybuddy/task.txt", "w") as file:
            pass #so that list is cleared
    #return 0

def print_task_list(task_list: list[str]) -> None:
    # grid = Table.grid(expand=True)
    # grid.add_column()
    # grid.add_column()
    # for idx, task in enumerate(task_list,start=1):
    #     grid.add_row(f"{idx}", f"{task}")

    # console.print(grid)
    table = Table(title="Task List", box=SIMPLE_HEAVY, min_width=10)
    for idx, task in enumerate(task_list,start=1):
        table.add_row(f"{idx}", f"{task}")
    console.print(table)
    #for each print??
    return;

def add_task(task_list: list[str]) -> None:
    task: str = input("\nAdding a task! Type contents here:")
    task_list.append(task)
    console.print(f" Task [magenta]{task}[/magenta] added!")

    return;

def edit_task(task_list: list[str]) -> None:
    #ask for new string
    #get new string
    #return it
    #idx = IntPrompt.ask("Which task do you want to edit?")
    while True:
        idx = IntPrompt.ask("\nWhich task would you like to edit?")
        if (idx > 0 and idx <= len(task_list)):
            break
        else:
            console.print("invalid option, try again", style="red")
    
    old_task = task_list[idx-1]
    console.print(f"old task: {old_task}")
    task: str = input("new task: ")
    task_list[idx-1] = task
    #return " "

def delete_task(task_list: list[str]) -> None:
    while True:
        idx = IntPrompt.ask("\nWhich task would you like to delete?")
        logger.info(f"{len(task_list)}")
        if (idx > 0 and idx <= len(task_list)):
            break
        else:
            console.print("invalid option, try again", style="red")
    
    console.print(f"Are you sure you want to delete task [magenta]{task_list[idx-1]}[/magenta]? [red]This action is irreversible![/red]")
    #conf = input("Type Y for yes, N for no:")
    conf = Prompt.ask("Type Y for yes, N for no:", choices=["Y", "N"])
    match conf:
        case "Y":
            task_list.pop(idx-1)
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
   # console.print("I Need Help!\nWelcome to Study Buddy!\nOn the home page:\nTo view your to do list, type v\nOnce you are viewing your to do list, type a to add to your list, or d to delete from your list\nTo add to your to do list, type a\nQuestions? Contact help@studybuddy.com!")
    console.print("Wondering how to get started?", style="bold")
    console.print("1. From the home page, type v to navigate to the view task page")
    console.print("2. type a to add a task. Start working on your task")
    console.print("3. Done with the task? Type d to delete. Want to change the task? Type e to edit!")
    return;

#use rich prompting!!!
def open_task_page(task_list: list[str]) -> None:
    while True:
        time.sleep(0.2)
        print_task_list(task_list)
        print("\nWant to work on your list?\n[magenta bold]a[/magenta bold] - add a task\n[magenta bold]d[/magenta bold] - delete a task\n[magenta bold]e[/magenta bold] - edit a task\n[red bold]exit[/red bold] - exit to do list\n")
        #option = input("enter command here:")
        option : str = Prompt.ask("enter command here", choices=["a", "d", "e", "exit"])
        match option:
            case "a":
                add_task(task_list)
            case "d":
                delete_task(task_list)
            case "e":
                edit_task(task_list)
            case "exit":
                console.print("\nExiting Task List!", style="bold")
                console.rule(style="magenta")
                break;
    #while loop
    #print list
    #print options list
    
def open_timer_page() -> None:
    #call a timer
    #close when they say exit
    #add timer info to a csv

    return

def render_summary_page() -> None:
    #call the report json func
    #print the data -> sum
    #unit conversion service here as well
    return

def render_motivational_quote() -> None:
    #call motivational quote func
    #pass into ascii art service
    return

def main() -> None:
    #logger.info("template-project")
    console.print("welcome to study buddy") #make this look pretty
    #call ascii art to make this look cute

    task_list: list[str] = []
    download_task_list(task_list)
    console.print("[bold]A study tool to help you keep track of your tasks so you can have a more efficient study session![/bold]\n")
    
    while True:
        console.print("Type the command and press enter to navigate to the page!", style = "bold")
        console.print("\n[magenta bold]v[/magenta bold] - view to do list\n[magenta bold]h[/magenta bold] - help page\n[magenta bold]a[/magenta bold] - add a task to list\n[magenta bold]t[/magenta bold] - start a timer\n[magenta bold]s[/magenta bold] - study session summary\n[magenta bold]q[/magenta bold] - generate motivational quote\n[red bold]exit[/red bold] - exit studdy buddy\n")
        option: str = Prompt.ask("enter command here", choices=["v", "h", "a", "exit"])
        console.rule(style="magenta")
        match (option):
            case "v":
                open_task_page(task_list)
            case "h":
                render_help_page()
            case "a":
                add_task(task_list)
            case "t":
                open_timer_page()
            case "s":
                render_summary_page()
            case "q":
                render_motivational_quote()
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
