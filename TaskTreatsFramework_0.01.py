class Task:
    def __init__(self, name, estimated_time):
        self.name = name
        self.estimated_time = estimated_time
        self.actual_time = None
        self.completed = False

class Reward:
    def __init__(self, name, time_value):
        self.name = name
        self.time_value = time_value

class TaskTreats:
    def __init__(self):
        self.tasks = []
        self.rewards = []
        self.data_visualizations = []

    def add_task(self, name, estimated_time):
        # Create a new task object and add it to the list of tasks
        task = Task(name, estimated_time)
        self.tasks.append(task)

    def edit_task(self, task_index, name=None, estimated_time=None):
        # Modify the attributes of the specified task
        task = self.tasks[task_index]
        if name is not None:
            task.name = name
        if estimated_time is not None:
            task.estimated_time = estimated_time

    def delete_task(self, task_index):
        # Remove the specified task from the list of tasks
        del self.tasks[task_index]

    def mark_task_completed(self, task_index, actual_time):
        # Mark the specified task as completed and record the actual time taken
        task = self.tasks[task_index]
        task.actual_time = actual_time
        task.completed = True

    def add_reward(self, name, time_value):
        # Create a new reward object and add it to the list of rewards
        reward = Reward(name, time_value)
        self.rewards.append(reward)

    def add_data_visualization(self, parameters):
        # Add the parameters for data visualization to the list of data visualizations
        self.data_visualizations.append(parameters)

    def view_tasks(self):
        # Print the details of all tasks, including their completion status
        for i, task in enumerate(self.tasks):
            status = "Completed" if task.completed else "Not completed"
            print(f"{i + 1}. {task.name} ({task.estimated_time} min) - {status}")

    def view_rewards(self):
        # Print the details of all rewards
        for reward in self.rewards:
            print(f"{reward.name} - {reward.time_value} min")

    def view_data_visualizations(self):
        # Print the details of all data visualizations
        for visualization in self.data_visualizations:
            print(visualization)


def get_int_input(prompt):
    # Helper function to get integer input from the user
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


task_treats = TaskTreats()

# Allow the user to input tasks and their estimated completion times
num_tasks = get_int_input("Enter the number of tasks: ")

for i in range(num_tasks):
    task_name = input(f"Enter the name of task {i + 1}: ")
    estimated_time = get_int_input("Enter the estimated completion time (in minutes): ")
    task_treats.add_task(task_name, estimated_time)

# Display the available options to the user
print("TaskTreats - Options:")
print("1. View current tasks")
print("2. Add a task")
print("3. Exit")

while True:
    option = get_int_input("Select an option: ")

    if option == 1:
        # View the current tasks
        print("Current Tasks:")
        task_treats.view_tasks()
    elif option == 2:
        # Allow the user to add a task
        task_name = input("Enter the name of the task: ")
        estimated_time = get_int_input("Enter the estimated completion time (in minutes): ")
        task_treats.add_task(task_name, estimated_time)
        print("Task added successfully!")
    elif option == 3:
        # Exit the program
        print("Exiting TaskTreats...")
        break
    else:
        print("Invalid option. Please try again.")
