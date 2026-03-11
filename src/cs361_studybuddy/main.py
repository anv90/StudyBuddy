from rich.box import SIMPLE_HEAVY
#from ssl import Options
from loguru import logger
from rich import print
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.console import Console
from datetime import date
import time
import requests
import json
console = Console()

def download_task_list()->list[str]:
    task_list = []
    try:
        with open("src/cs361_studybuddy/task.txt", "r") as file:
            for line in file:
                task = line.strip()
                if task:
                    task_list.append(task)
    except FileNotFoundError:
        #logger.error("file not found")
        return task_list
    else:
        #logger.info("file found")
        return task_list

def upload_task_list(task_list: list[str]):
    if(len(task_list) > 0):
        with open("src/cs361_studybuddy/task.txt", "w") as file:
            for line in task_list:
                file.write(f"{line}\n")
    else:
        with open("src/cs361_studybuddy/task.txt", "w") as file:
            pass #so that list is cleared
    

def print_task_list(task_list: list[str]) -> None:
    table = Table(title="Task List", box=SIMPLE_HEAVY, min_width=10)
    table.add_column("ID", justify="right")
    table.add_column("Task")
    for idx, task in enumerate(task_list,start=1):
        table.add_row(f"{idx}", f"{task}")
    console.print(table)
    #for each print??
    return

def add_task(task_list: list[str]) -> None:
    task: str = input("\nAdding a task! Type contents here:")
    task_list.append(task)
    console.print(f" Task [magenta]{task}[/magenta] added!")

    return

def edit_task(task_list: list[str]) -> None:
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

def delete_task(task_list: list[str]) -> None:
    while True:
        idx = IntPrompt.ask("\nWhich task would you like to delete?")
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


def render_help_page() -> None:
    
   # console.print("I Need Help!\nWelcome to Study Buddy!\nOn the home page:\nTo view your to do list, type v\nOnce you are viewing your to do list, type a to add to your list, or d to delete from your list\nTo add to your to do list, type a\nQuestions? Contact help@studybuddy.com!")
    console.print("Wondering how to get started?", style="bold")
    console.print("1. From the home page, type v to navigate to the view task page")
    console.print("2. type a to add a task. Start working on your task")
    console.print("3. Done with the task? Type d to delete. Want to change the task? Type e to edit!")
    return


def open_task_page(task_list: list[str]) -> None:
    console.print(f"[yellow]DEBUG: List has {len(task_list)} items.[/yellow]")
    while True:
        #time.sleep(0.2)
        print_task_list(task_list)
        console.print("\nWant to work on your list?\n[magenta bold]a[/magenta bold] - add a task\n[magenta bold]d[/magenta bold] - delete a task\n[magenta bold]e[/magenta bold] - edit a task\n[red bold]exit[/red bold] - exit to do list\n")
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
                break
   
    
def open_timer_page() -> None:
    #call a timer
    #close when they say exit
    #add timer info to a csv
    #prompt for duration and count
    info = Prompt.ask("\nWhat do you want to focus on today?")
    duration = IntPrompt.ask("\nHow long would you like your timer (in minutes)?")
    
    unit_response = requests.get(f"http://localhost:6001/unit-conversion?num={duration}&unit=min")
    if unit_response.status_code != 200:
        console.print(f"{unit_response.text}")
    conversion = unit_response.json()
    logger.info(conversion["sec"])
    timer_info = {"count":1,"duration":int(conversion['sec'])}
    post_response = requests.post(f"http://localhost:8000/timer/set-timer", json=timer_info)
    if post_response.status_code == 200:
        timer_id = post_response.json().get('timer id', 0)
        console.print("Here's some music while you wait:")
        music_response = requests.get(f"http://localhost:2500/music")
        if music_response.status_code == 200:
            console.print(music_response.json())
        else: 
            console.print(music_response.text)
       
        while (True):
            time.sleep(60)
            get_response = requests.get(f"http://localhost:8000/timer/{timer_id}/details")
            result = get_response.json() 
            if get_response.status_code == 200:
                result = get_response.json()
                time_left = result.get('time_remaining', 0)
                state = result.get('state')
                if (time_left <= 0 or state == "inactive"):
                    break
                print(f"{time_left} + {state}") 
            else:
                console.print(f"{get_response.status_code}")
        with open("src/cs361_studybuddy/timer_data.json", "a") as file:
            session_info = {"task": info, "time": duration, "date": date.today().isoformat()}
            json.dump(session_info, file, indent=4)
        console.print("timer has ended!")

    else: 
        console.print(f"{post_response.text}")
        

    return

def render_summary_page() -> None:
    #call the report json func
    #print the data -> sum
    #unit conversion service here as well
    with open("src/cs361_studybuddy/timer_data.json", "r") as file:
        session_data = json.load(file)
    timer_json = {"report": {
        "title": "Study Session Summary",
        "operation": "sum",
        "operation_field": "time",
        "filter_field": "",
        "filter_value": "",
        "date_field": "",
        "date_range": {
            "from": "",
            "to": ""
        }
    },
    "data": session_data
    }
    response = requests.post(f"http://localhost:5001/report", json=timer_json)
    result = response.json()
    if response.status_code == 200:
        total = result.get('result', 0)
        unit_response = requests.get(f"http://localhost:6001/unit-conversion?num={total}&unit=min")
        if unit_response.status_code != 200:
            console.print(f"{unit_response.text}")
            conversion = unit_response.json()
        console.print(f"You focused for a total of {total} minutes!")
        console.print(f"That's equal to {conversion["days"]} days!")
    else:
        console.print(response.text)

def render_motivational_quote() -> None:
    response = requests.get(f"http://localhost:1400/quotes/1")
    if response.status_code == 200:
        quote = response.json()
        quote_json = {"message":quote[0], "sprite":True}
        response = requests.post("http://localhost:8000/ascii", json=quote_json)
        if response.status_code == 200:
            result = response.json()
            console.print(result["message"])
        else:
            console.print(response.text)
    else:
        console.print(response.text)

    return

def main() -> None:
    #logger.info("template-project")
    title_json = {"message":"welcome to study buddy", "sprite":False}
    response = requests.post("http://localhost:8000/ascii", json=title_json)
    if response.status_code == 200:
        result = response.json()
        console.print(result["message"]) 

    task_list: list[str] = []
    task_list = download_task_list()
    console.print("[bold]A study tool to help you keep track of your tasks so you can have a more efficient study session![/bold]\n")
    
    while True:
        console.print("Type the command and press enter to navigate to the page!", style = "bold")
        console.print("\n[magenta bold]v[/magenta bold] - view to do list\n[magenta bold]h[/magenta bold] - help page\n[magenta bold]a[/magenta bold] - add a task to list\n[magenta bold]t[/magenta bold] - start a timer\n[magenta bold]s[/magenta bold] - study session summary\n[magenta bold]q[/magenta bold] - generate motivational quote\n[red bold]exit[/red bold] - exit studdy buddy\n")
        option: str = Prompt.ask("enter command here", choices=["v", "h", "a", "t","s","q", "exit"])
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
