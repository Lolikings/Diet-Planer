# Importing tkinter and sqlite3 modules
import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
# Creating a database connection and a cursor object
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Creating a table to store user data
c.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    age INTEGER,
    gender TEXT,
    weight REAL,
    height REAL,
    goal TEXT
)""")

# Committing changes and closing the connection
conn.commit()
conn.close()

# Defining a class for the start screen
class StartScreen(tk.Frame):
    def __init__(self, master):
        # Initializing the frame
        tk.Frame.__init__(self, master)
        self.master = master

        # Creating widgets for the start screen
        self.title = tk.Label(self, text="Welcome to the Diet Planner App", font=("Arial", 20))
        self.start_button = tk.Button(self, text="Start", command=self.go_to_form)
        self.exit_button = tk.Button(self, text="Exit", command=self.master.destroy)
        self.show_users_button = tk.Button(self, text="Show All Users", command=self.show_users)

        # Placing the widgets on the screen
        self.title.pack(pady=20)
        self.start_button.pack(pady=10)
        self.exit_button.pack(pady=10)
        self.show_users_button.pack(pady=10)

    # Defining a function to go to the form screen
    def go_to_form(self):
        # Creating an instance of the form screen and placing it on top of the start screen
        self.form_screen = FormScreen(self.master)
        self.form_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)


 # Defining a function to show all users in a new window
    def show_users(self):
        # Creating a new window and a treeview widget
        self.users_window = tk.Toplevel(self.master)
        self.users_window.title("All Users")
        self.users_treeview = tk.ttk.Treeview(self.users_window)

        # Defining the columns and headings for the treeview
        self.users_treeview["columns"] = ("name", "age", "gender", "weight", "height", "goal")
        self.users_treeview.column("#0", width=0, stretch=tk.NO)
        self.users_treeview.column("name", anchor=tk.W, width=120)
        self.users_treeview.column("age", anchor=tk.CENTER, width=80)
        self.users_treeview.column("gender", anchor=tk.CENTER, width=80)
        self.users_treeview.column("weight", anchor=tk.CENTER, width=80)
        self.users_treeview.column("height", anchor=tk.CENTER, width=80)
        self.users_treeview.column("goal", anchor=tk.CENTER, width=80)
        self.users_treeview.heading("#0", text="", anchor=tk.W)
        self.users_treeview.heading("name", text="Name", anchor=tk.W)
        self.users_treeview.heading("age", text="Age", anchor=tk.CENTER)
        self.users_treeview.heading("gender", text="Gender", anchor=tk.CENTER)
        self.users_treeview.heading("weight", text="Weight (kg)", anchor=tk.CENTER)
        self.users_treeview.heading("height", text="Height (cm)", anchor=tk.CENTER)
        self.users_treeview.heading("goal", text="Goal", anchor=tk.CENTER)

        # Connecting to the database and fetching all user data
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()

        # Inserting each user data as a row into the treeview
        for user in users:
            self.users_treeview.insert(parent="", index="end", values=user)

        # Closing the database connection
        conn.close()

        # Creating buttons for updating and deleting selected user
        self.update_button = tk.Button(self.users_window, text="Update User", command=self.update_user_from_list)
        self.delete_button = tk.Button(self.users_window, text="Delete User", command=self.delete_user_from_list)

        # Placing the treeview and buttons on the window
        self.users_treeview.pack(fill=tk.BOTH, expand=True)
        self.update_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Defining a function to update the user data from the list
    def update_user_from_list(self):
        # Getting the selected item from the treeview
        cur_id = self.users_treeview.focus()
        
        # Checking if any item is selected
        if cur_id:
            # Getting the user data from the item values
            name, age, gender, weight, height, goal = self.users_treeview.item(cur_id)["values"]

            # Creating an instance of the update screen and passing the user data as arguments
            self.update_screen = UpdateScreen(self.master, name, age, gender, weight, height, goal)

            # Placing the update screen on top of the start screen
            self.update_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)

            # Destroying the users window
            self.users_window.destroy()
        
    # Defining a function to delete the user data from the list
    def delete_user_from_list(self):
        # Getting the selected item from the treeview
        cur_id = self.users_treeview.focus()

         # Checking if any item is selected
        if cur_id:
             # Getting the user email from the item iid
            name = cur_id

             # Connecting to the database and deleting the user data from the table
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE name = ?", (name,))
            conn.commit()
            conn.close()

             # Deleting the item from the treeview
            self.users_treeview.delete(cur_id)


# Defining a class for the form screen
class FormScreen(tk.Frame):
    def __init__(self, master):
        # Initializing the frame
        tk.Frame.__init__(self, master)
        self.master = master

        # Creating widgets for the form screen
        self.title = tk.Label(self, text="Please fill in your details", font=("Arial", 20), padx=10, pady=10)
        self.name_label = tk.Label(self, text="Name:", padx=10, pady=10)
        self.name_entry = tk.Entry(self)
        self.age_label = tk.Label(self, text="Age:", padx=10, pady=10)
        self.age_entry = tk.Entry(self)
        self.gender_label = tk.Label(self, text="Gender:", padx=10, pady=10)
        self.gender_combobox = tk.ttk.Combobox(self, values=["Male", "Female", "Other"])
        self.weight_label = tk.Label(self, text="Weight (in kg):", padx=10, pady=10)
        self.weight_entry = tk.Entry(self)
        self.height_label = tk.Label(self, text="Height (in cm):", padx=10, pady=10)
        self.height_entry = tk.Entry(self)
        self.goal_label = tk.Label(self, text="Goal:", padx=10, pady=10)
        self.goal_combobox = tk.ttk.Combobox(self, values=["Maintain", "Gain", "Lose"])
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_data, padx=10, pady=10)


        # Placing the widgets on the screen using a grid layout
        self.title.grid(row=0, column=0, columnspan=2, pady=20)
        self.name_label.grid(row=1, column=0, sticky=tk.E)
        self.name_entry.grid(row=1, column=1)
        self.age_label.grid(row=2, column=0, sticky=tk.E)
        self.age_entry.grid(row=2, column=1)
        self.gender_label.grid(row=3, column=0, sticky=tk.E)
        self.gender_combobox.grid(row=3, column=1)
        self.weight_label.grid(row=4, column=0, sticky=tk.E)
        self.weight_entry.grid(row=4, column=1)
        self.height_label.grid(row=5, column=0, sticky=tk.E)
        self.height_entry.grid(row=5, column=1)
        self.goal_label.grid(row=6, column=0, sticky=tk.E)
        self.goal_combobox.grid(row=6, column=1)
        self.submit_button.grid(row=7, column=0, columnspan=2)

    # Defining a function to submit the user data and go to the next screen

    def submit_data(self):
        # Getting the user input from the entry and combobox widgets
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_combobox.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()
        goal = self.goal_combobox.get()

        # Checking if any of the fields are empty
        if not name or not age or not gender or not weight or not height or not goal:
            # Creating a messagebox widget to show a warning message
            tk.messagebox.showwarning(title="Warning", message="Please fill in all the fields.")
            return # Returning from the function without proceeding further

        # Converting the age, weight and height to numeric values
        age = int(age)
        weight = float(weight)
        height = float(height)

        # Connecting to the database and inserting the user data into the table
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (name, age, gender, weight, height, goal))
        conn.commit()
        conn.close()

        # Calculating the BMI and generating the diet plan for the user
        bmi = calculate_bmi(weight, height)
        diet_plan = generate_diet_plan(bmi, gender, age)

        # Creating an instance of the next screen and passing the user data and diet plan as arguments
        self.next_screen = NextScreen(self.master, name, age, gender, weight, height, goal, bmi, diet_plan)
        self.next_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)



# Defining a class for the next screen
class NextScreen(tk.Frame):
    def __init__(self, master, name, age, gender, weight, height, goal, bmi, diet_plan):
        # Initializing the frame
        tk.Frame.__init__(self, master)
        self.master = master

        # Creating widgets for the next screen
        self.title = tk.Label(self, text="Your Diet Plan", font=("Arial", 20))
        self.name_label = tk.Label(self, text=f"Name: {name}")
        self.age_label = tk.Label(self, text=f"Age: {age}")
        self.gender_label = tk.Label(self, text=f"Gender: {gender}")
        self.weight_label = tk.Label(self, text=f"Weight: {weight} kg")
        self.height_label = tk.Label(self, text=f"Height: {height} cm")
        self.goal_label = tk.Label(self, text=f"Goal: {goal}")
        self.bmi_label = tk.Label(self, text=f"BMI: {bmi}")
        self.diet_plan_label = tk.Label(self, text="Diet Plan:")
        self.diet_plan_text = tk.Text(self)
        self.diet_plan_text.insert(tk.END, diet_plan)

        self.main_menu_button = tk.Button(self, text="Return to Main Menu", command=self.go_to_main_menu)
        self.update_user_button = tk.Button(self, text="Update User", command=self.update_user)
        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)

        # Placing the widgets on the screen using a grid layout
        self.title.grid(row=0, column=0, columnspan=2, pady=20)
        self.name_label.grid(row=1, column=0)
        self.age_label.grid(row=2, column=0)
        self.gender_label.grid(row=3, column=0)
        self.weight_label.grid(row=4, column=0)
        self.height_label.grid(row=5, column=0)
        self.goal_label.grid(row=6, column=0)
        self.bmi_label.grid(row=7, column=0)
        self.diet_plan_label.grid(row=8, column=0)
        self.diet_plan_text.grid(row=9,pady=50, columnspan=2)
        self.main_menu_button.grid(row=10, column=0)
        self.update_user_button.grid(row=10, column=1)
        self.quit_button.grid(row=11, column=0, columnspan=2)

    # Defining a function to go back to the main menu
    def go_to_main_menu(self):
        # Creating an instance of the start screen and placing it on top of the next screen
        self.start_screen = StartScreen(self.master)
        self.start_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)

    # Defining a function to update the user data
    def update_user(self):
        # Getting the current user data from the labels
        name = self.name_label.cget("text").split(": ")[1]
        age = int(self.age_label.cget("text").split(": ")[1])
        gender = self.gender_label.cget("text").split(": ")[1]
        weight = float(self.weight_label.cget("text").split(": ")[1].split(" ")[0])
        height = float(self.height_label.cget("text").split(": ")[1].split(" ")[0])
        goal = self.goal_label.cget("text").split(": ")[1]

# Creating an instance of the update screen and passing the current user data as arguments
        self.update_screen = UpdateScreen(self.master, name, age, gender, weight, height, goal)
        self.update_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)


# Defining a class for the update screen
class UpdateScreen(tk.Frame):
    def __init__(self, master, name, age, gender, weight, height, goal):
        # Initializing the frame
        tk.Frame.__init__(self, master)
        self.master = master

        # Creating widgets for the update screen
        self.title = tk.Label(self, text="Please edit your details", font=("Arial", 20))
        self.name_label = tk.Label(self, text="Name:", padx=10, pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, name) # Inserting the current name into the entry widget
        self.age_label = tk.Label(self, text="Age:", padx=10, pady=10)
        self.age_entry = tk.Entry(self)
        self.age_entry.insert(0, age) # Inserting the current age into the entry widget
        self.gender_label = tk.Label(self, text="Gender:", padx=10, pady=10)
        self.gender_combobox = tk.ttk.Combobox(self, values=["Male", "Female", "Other"])
        self.gender_combobox.set(gender) # Setting the current gender into the combobox widget
        self.weight_label = tk.Label(self, text="Weight (in kg):", padx=10, pady=10)
        self.weight_entry = tk.Entry(self)
        self.weight_entry.insert(0, weight) # Inserting the current weight into the entry widget
        self.height_label = tk.Label(self, text="Height (in cm):", padx=10, pady=10)
        self.height_entry = tk.Entry(self)
        self.height_entry.insert(0, height) # Inserting the current height into the entry widget
        self.goal_label = tk.Label(self, text="Goal:", padx=10, pady=10)
        self.goal_combobox = tk.ttk.Combobox(self, values=["Maintain", "Gain", "Lose"])
        self.goal_combobox.set(goal) # Setting the current goal into the combobox widget
        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel, padx=10, pady=10)


        # Placing the widgets on the screen using a grid layout
        self.title.grid(row=0, column=0, columnspan=2, pady=20)
        self.name_label.grid(row=1, column=0, sticky=tk.E)
        self.name_entry.grid(row=1, column=1)
        self.age_label.grid(row=2, column=0, sticky=tk.E)
        self.age_entry.grid(row=2, column=1)
        self.gender_label.grid(row=3, column=0, sticky=tk.E)
        self.gender_combobox.grid(row=3, column=1)
        self.weight_label.grid(row=4, column=0, sticky=tk.E)
        self.weight_entry.grid(row=4, column=1)
        self.height_label.grid(row=5, column=0, sticky=tk.E)
        self.height_entry.grid(row=5, column=1)
        self.goal_label.grid(row=6, column=0, sticky=tk.E)
        self.goal_combobox.grid(row=6, column=1)
        self.save_button.grid(row=7, column=0)
        self.cancel_button.grid(row=7, column=1)

    # Defining a function to save the edited user data and go back to the previous screen
    def save_data(self):
        # Getting the user input from the entry and combobox widgets
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        gender = self.gender_combobox.get()
        weight = float(self.weight_entry.get())
        height = float(self.height_entry.get())
        goal = self.goal_combobox.get()


        # Connecting to the database and updating the user data in the table
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET name = ?, age = ?, gender = ?, weight = ?, height = ?, goal = ? WHERE name = ?", (name, age, gender, weight, height, goal, name))
        conn.commit()
        conn.close()

        # Calculating the BMI and generating the diet plan for the user
        bmi = calculate_bmi(weight, height)
        diet_plan = generate_diet_plan(bmi, gender, age)

        # Creating an instance of the previous screen and passing the updated user data and diet plan as arguments
        self.previous_screen = NextScreen(self.master, name, age, gender, weight, height, goal, bmi, diet_plan)
        self.previous_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)

    # Defining a function to cancel the editing and go back to the previous screen
    # Defining a function to cancel the editing and go back to the previous screen
    # Defining a function to cancel the editing and go back to the previous screen
    def cancel(self):
        # Getting the current user data from the labels
        name = self.name_label.cget("text").split(": ")
        if len(name) > 1:
            name = name[1]
        else:
            name = ""
        age = self.age_label.cget("text").split(": ")
        if len(age) > 1:
            age = int(age[1])
        else:
            age = 0
        gender = self.gender_label.cget("text").split(": ")
        if len(gender) > 1:
            gender = gender[1]
        else:
            gender = ""
        weight = self.weight_label.cget("text").split(": ")
        if len(weight) > 1:
            weight = float(weight[1].split(" ")[0])
        else:
            weight = 1
        height = self.height_label.cget("text").split(": ")
        if len(height) > 1:
            height = float(height[1].split(" ")[0])
        else:
            height = 1
        goal = self.goal_label.cget("text").split(": ")
        if len(goal) > 1:
            goal = goal[1]
        else:
            goal = ""

        # Calculating the BMI and generating the diet plan for the user
        bmi = calculate_bmi(weight, height)
        diet_plan = generate_diet_plan(bmi, gender, age)

        # Creating an instance of the previous screen and passing the current user data and diet plan as arguments
        user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "goal": goal,
            "bmi": bmi,
            "diet_plan": diet_plan
        }
        self.previous_screen = NextScreen(self.master, **user_data)
        self.previous_screen.place(in_=self.master, x=0, y=0, relwidth=1, relheight=1)

# Defining a function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height / 100) ** 2, 1)

# Defining a function to generate diet plan based on BMI, gender and age
def generate_diet_plan(bmi, gender, age):
    # Defining some sample diet plans for different categories
    underweight_male = """Breakfast: Oatmeal with milk and nuts
Lunch: Chicken sandwich with cheese and salad
Dinner: Salmon with rice and vegetables
Snacks: Yogurt, fruit, granola bars"""

    underweight_female = """Breakfast: Scrambled eggs with toast and butter
Lunch: Pasta with meat sauce and cheese
Dinner: Beef stew with potatoes and carrots
Snacks: Smoothies, nuts, chocolate"""

    normal_male = """Breakfast: Cereal with milk and fruit
Lunch: Turkey wrap with lettuce and tomato
Dinner: Chicken curry with naan bread and salad
Snacks: Hummus, crackers, cheese"""

    normal_female = """Breakfast: Pancakes with maple syrup and berries
Lunch: Vegetable soup with bread and butter
Dinner: Stir-fry with tofu and noodles
Snacks: Popcorn, cookies, milk"""

    overweight_male = """Breakfast: Greek yogurt with granola and fruit
Lunch: Salad with grilled chicken and dressing
Dinner: Roasted turkey with quinoa and broccoli
Snacks: Almonds, apple slices, celery sticks"""

    overweight_female = """Breakfast: Omelet with spinach and cheese
Lunch: Sandwich with ham and cheese on whole wheat bread
Dinner: Grilled fish with brown rice and asparagus
Snacks: Carrot sticks, peanut butter, orange"""

    # Determining the category based on BMI, gender and age
    if bmi < 18.5:
        category = "underweight"
    elif bmi >= 18.5 and bmi < 25:
        category = "normal"
    else:
        category = "overweight"

    if gender == "Male":
        category += "_male"
    else:
        category += "_female"

# Returning the diet plan for the category
    return locals()[category]


# Creating the main window and an instance of the start screen
root = tk.Tk()
root.title("Diet Planner App")
root.geometry("800x800")
start_screen = StartScreen(root)
start_screen.pack(fill=tk.BOTH, expand=True)

# Running the main loop
root.mainloop()
