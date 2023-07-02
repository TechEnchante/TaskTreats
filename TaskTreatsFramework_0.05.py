import sqlite3
import bcrypt
import time

#oh...hi, welcome to my code.
#I should probably comment this later. *shrug* you can probably figure it out...
#JK, got you good. Okay but yeah, this is task treats.


# Prints the Task Treats banner
def print_banner():

    print(
        r"""
     ______   ______     ______     __  __        ______   ______     ______     ______     ______   ______    
    /\__  _\ /\  __ \   /\  ___\   /\ \/ /       /\__  _\ /\  == \   /\  ___\   /\  __ \   /\__  _\ /\  ___\   
    \/_/\ \/ \ \  __ \  \ \___  \  \ \  _"-.     \/_/\ \/ \ \  __<   \ \  __\   \ \  __ \  \/_/\ \/ \ \___  \  
       \ \_\  \ \_\ \_\  \/\_____\  \ \_\ \_\       \ \_\  \ \_\ \_\  \ \_____\  \ \_\ \_\    \ \_\  \/\_____\ 
        \/_/   \/_/\/_/   \/_____/   \/_/\/_/        \/_/   \/_/ /_/   \/_____/   \/_/\/_/     \/_/   \/_____/ 

    Task Treats: written by Adam Roberts aka TechEnchante"""
    )

#I should probably comment this later. *shrug* you can probably figure it out...
#JK, got you good. Okay but yeah, this is task treats.

# Represents a User with username and password attributes
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Verifies the given password with the user's password
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)

# Represents a Task with name, estimated_time, actual_time, and completed attributes
class Task:
    def __init__(self, name, estimated_time):
        self.name = name
        self.estimated_time = estimated_time
        self.actual_time = None
        self.completed = False

# Represents a Reward with name and time_value attributes
#(The rewards database/logic are coming later)
class Reward:
    def __init__(self, name, time_value):
        self.name = name
        self.time_value = time_value

# Represents the Task Treats application with a user, tasks, rewards, and data visualizations
#(Again, the rewards and data visualizations are coming later)
class TaskTreats:
    def __init__(self, user):
        self.user = user
        self.tasks = []
        self.rewards = []
        self.data_visualizations = []

    # Adds a new task with the given name and estimated time
    def add_task(self, name, estimated_time):
        task = Task(name, estimated_time)
        self.tasks.append(task)

        conn = sqlite3.connect("tasktreats.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO tasks VALUES (?, ?, ?, ?, ?)",
            (
                self.user.username,
                task.name,
                task.estimated_time,
                task.actual_time,
                task.completed,
            ),
        )
        conn.commit()
        conn.close()

    # Views all tasks associated with the user, including their details
    def view_all_tasks(self):
        conn = sqlite3.connect("tasktreats.db")
        c = conn.cursor()
        c.execute(
            "SELECT name, estimated_time, actual_time, completed FROM tasks WHERE username = ?",
            (self.user.username,),
        )
        tasks = c.fetchall()
        conn.close()

        if tasks:
            for i, (name, estimated_time, actual_time, completed) in enumerate(tasks):
                status = "Completed" if completed else "Not completed"
                print(f"{i + 1}. {name} ({estimated_time} min) - {status}")
        else:
            print("No tasks found.")

    # Edits a task's details, such as name or estimated time
    def edit_task(self, task_index, name=None, estimated_time=None):
        task = self.tasks[task_index]
        if name is not None:
            task.name = name
        if estimated_time is not None:
            task.estimated_time = estimated_time

        conn = sqlite3.connect("tasktreats.db")
        c = conn.cursor()
        c.execute(
            "UPDATE tasks SET name = ?, estimated_time = ?, actual_time = ?, completed = ? WHERE username = ? AND name = ?",
            (
                task.name,
                task.estimated_time,
                task.actual_time,
                task.completed,
                self.user.username,
                task.name,
            ),
        )
        conn.commit()
        conn.close()

    # Marks a task as completed with the given actual time
    def mark_task_completed(self, task_index, actual_time):
        task = self.tasks[task_index]
        task.actual_time = actual_time
        task.completed = True

        conn = sqlite3.connect("tasktreats.db")
        c = conn.cursor()
        c.execute(
            "UPDATE tasks SET actual_time = ?, completed = ? WHERE username = ? AND name = ?",
            (task.actual_time, task.completed, self.user.username, task.name),
        )
        conn.commit()
        conn.close()

    # Adds a reward with the given name and time value
    #(Coming later. When? HAHAHAHAHA, like I know)
    def add_reward(self, name, time_value):
        reward = Reward(name, time_value)
        self.rewards.append(reward)

    # Adds a data visualization with the given parameters
    #(Coming later, working on a data visualization platform)
    def add_data_visualization(self, parameters):
        self.data_visualizations.append(parameters)

    # Views the current tasks that are not completed
    def view_current_tasks(self):
        current_tasks = [task for task in self.tasks if not task.completed]

        if not current_tasks:
            print("You don't have any current tasks!")
            return

        for i, task in enumerate(current_tasks):
            print(f"{i + 1}. {task.name} ({task.estimated_time} min) - To-Do")

    # Views all the rewards with their names and time values
    #(Coming later. Getting sick of reading that huh? I am sick of writting it)
    def view_rewards(self):
        for reward in self.rewards:
            print(f"{reward.name} - {reward.time_value} min")

    # Views all the data visualizations
    # (C...urrently in progress. You thought I was going to say "Coming later" again :P)
    def view_data_visualizations(self):
        for visualization in self.data_visualizations:
            print(visualization)

# Retrieves an integer input from the user with optional minimum value validation
def get_int_input(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(
                    f"Invalid input. Please enter an integer greater than or equal to {min_value}."
                )
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Retrieves a string input from the user with optional empty string validation
def get_str_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("Invalid input. Please enter a non-empty string.")
        else:
            return value if value else None

# Initializes the Task Treats database
def initialize_database():
    conn = sqlite3.connect("tasktreats.db")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, password TEXT)
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks
        (username TEXT, name TEXT, estimated_time INT, actual_time INT, completed BOOLEAN)
    """
    )

    conn.commit()
    conn.close()

# Allows a user to sign in to the Task Treats application, need to impliment a password change option.
def sign_in():
    username = get_str_input("Enter your username: ")
    password = get_str_input("Enter your password: ")

    conn = sqlite3.connect("tasktreats.db")
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    conn.close()

    if result is None:
        print("No user found with that username.")
        return None

    hashed_password = result[0]

    if not bcrypt.checkpw(password.encode(), hashed_password.encode()):
        print("Incorrect password.")
        return None

    user = User(username, hashed_password)

    conn = sqlite3.connect("tasktreats.db")
    c = conn.cursor()
    c.execute(
        "SELECT name, estimated_time, actual_time, completed FROM tasks WHERE username = ?",
        (username,),
    )
    tasks = c.fetchall()

    task_treats = TaskTreats(user)
    for name, estimated_time, actual_time, completed in tasks:
        task = Task(name, estimated_time)
        task.actual_time = actual_time
        task.completed = completed
        task_treats.tasks.append(task)

    conn.close()

    return task_treats

# Allows a user to sign up for the Task Treats application
def sign_up():
    username = get_str_input("Enter a username: ")
    password = get_str_input("DO NOT LOSE YOUR PASSWORD, NO CURRENT WAY TO RECOVER IT!!! Enter a password: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = sqlite3.connect("tasktreats.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
    except sqlite3.IntegrityError:
        print("Username already taken.")
        return None

    conn.commit()
    conn.close()

    return User(username, hashed_password)

# Initializing the database for TaskTreats
initialize_database()

# Displaying the Sign In / Sign Up options
print("TaskTreats - Sign In / Sign Up")
print("1. Sign In")
print("2. Sign Up")

while True:
    # Prompting the user to select an option.
    option = get_int_input("Select an option: ", min_value=1)

    if option == 1:
        task_treats = sign_in()
        if task_treats is not None:
            # Displaying the TaskTreats banner after successful sign-in, because it deserves a grand entrance.
            print_banner()
            break
    elif option == 2:
        # Signing up a new user, because it's time for you to look inward and start asking yourself the big question: who are you and what do you want?
        user = sign_up()
        if user is not None:
            task_treats = TaskTreats(user)
            # Creating a TaskTreats instance for the new user and displaying the banner, let the journey begin!
            print_banner()
            break
    else:
        print("Invalid option. Please try again.")

while True:

    print("\nTaskTreats - Options:")
    print("1. Add Tasks")
    print("2. View current tasks")
    print("3. View all tasks including completed")
    print("4. Modify a task")
    print("5. Mark task(s) as done")
    print("6. Exit")

    option = get_int_input("\nSelect an option: ", min_value=1)

    if option == 1:
        # Adding tasks, because more tasks mean more opportunities for triumph (or procrastination)
        num_tasks = get_int_input("Enter the number of tasks to add: ", min_value=1)

        for i in range(num_tasks):
            task_name = get_str_input(f"Enter the name of task {i + 1}: ")
            estimated_time = get_int_input(
                "Enter the estimated completion time (in minutes): ", min_value=1
            )
            task_treats.add_task(task_name, estimated_time)
            print("Task(s) added successfully!")

    elif option == 2:
        # Viewing current tasks, let's see what battles lie ahead (or what you've been putting off)
        print("Current Tasks:")
        task_treats.view_current_tasks()
        time.sleep(3)

    elif option == 3:
        # Viewing all tasks, because sometimes you need to reflect on your past conquests (or failures)
        print("All Tasks:")
        task_treats.view_all_tasks()
        time.sleep(3)

    elif option == 4:

        if not task_treats.tasks or not any(
            not task.completed for task in task_treats.tasks
        ):
            print("You don't have any current tasks!")

            time.sleep(3)

            continue

        # Modifying a task, because change is the only constant (except for your procrastination)
        task_index = get_int_input(
            "Enter the index of the task to modify: ", min_value=1
        )

        new_name = get_str_input(
            "Enter the new name (or leave blank to keep the existing name): ",
            allow_empty=True,
        )

        new_estimated_time = get_int_input(
            "Enter the new estimated completion time (in minutes) (or 0 to keep the existing time): ",
            min_value=0,
        )

        task_treats.edit_task(
            task_index - 1, name=new_name, estimated_time=new_estimated_time or None
        )

        print("Task modified successfully!")

    elif option == 5:

        if not task_treats.tasks or not any(
            not task.completed for task in task_treats.tasks
        ):
            print("You don't have any current tasks!")

            time.sleep(3)

            continue

        # Marking tasks as done, because crossing things off the list is a satisfying victory (or relief)
        task_treats.view_current_tasks()

        task_indices = input(
            "Enter the index/indices of the tasks to mark as done (separated by commas): "
        )

        task_indices = [int(idx.strip()) for idx in task_indices.split(",")]

        actual_time = get_int_input(
            "Enter the actual time taken to complete the task (in minutes): ",
            min_value=1,
        )

        for task_index in task_indices:

            if 1 <= task_index <= len(task_treats.tasks):
                task_treats.mark_task_completed(task_index - 1, actual_time)
            else:
                print(f"Invalid task index: {task_index}. Skipping...")

        print("Task(s) marked as done successfully!")

    elif option == 6:
        # Exiting TaskTreats, until we meet again on the battlefield of productivity. Now come back soon yall, ya hear?
        print("Exiting TaskTreats...")
        break
    else:
        print("Invalid option. Please try again.")

