import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import json
import subprocess
import sys  # Import the sys module

# Function to create and optionally open a new code file
def create_code_file(open_file=False):
    selected_language = language_var.get()
    file_name = name_entry.get()
    
    if not file_name:
        result_label.config(text="Please enter a file name.")
        return
    
    file_extension = {
        "HTML": ".html",
        "CSS": ".css",
        "Python": ".py",
        "JavaScript": ".js",
        "PHP": ".php"
    }
    
    extension = file_extension[selected_language]
    
    if custom_path:
        file_path = os.path.join(custom_path, file_name + extension)
    else:
        file_path = os.path.join(default_path, file_name + extension)
    
    if os.path.exists(file_path):
        result_label.config(text="File already exists.")
    else:
        with open(file_path, "w") as file:
            result_label.config(text=f"{selected_language} file created: {file_path}")
            name_entry.delete(0, "end")
            if open_file:
                open_generated_file(file_path)

def open_generated_file(file_path):
    if sys.platform.startswith('win'):
        os.startfile(file_path)
    else:
        subprocess.Popen(['xdg-open', file_path])

def save_custom_path():
    global custom_path
    custom_path = filedialog.askdirectory()
    with open("custom_path.json", "w") as config_file:
        json.dump({"custom_path": custom_path}, config_file)
    custom_path_label.config(text=f"Custom Path: {custom_path}")

# Create the main application window
app = tk.Tk()
app.title("Code File Generator")

# Create a label
label = ttk.Label(app, text="Choose a programming language and enter a file name:")
label.pack()

# Create a dropdown to select the programming language
languages = ["HTML", "CSS", "Python", "JavaScript", "PHP"]
language_var = tk.StringVar(value=languages[0])
language_dropdown = ttk.Combobox(app, textvariable=language_var, values=languages)
language_dropdown.pack()

# Create an entry for the file name
name_label = ttk.Label(app, text="File Name:")
name_label.pack()
name_entry = ttk.Entry(app)
name_entry.pack()

# Create a button to create the code file
create_button = ttk.Button(app, text="Create File", command=lambda: create_code_file(open_after_creation.get()))
create_button.pack()

# Create a label to display the result
result_label = ttk.Label(app, text="")
result_label.pack()

# Default path (Desktop)
default_path = os.path.expanduser("~/Desktop")
custom_path = ""

# Load custom path from a configuration file if it exists
config_file_path = "custom_path.json"
if os.path.exists(config_file_path):
    with open(config_file_path, "r") as config_file:
        config = json.load(config_file)
        custom_path = config.get("custom_path", "")

# Create a button to choose a custom path
choose_custom_path_button = ttk.Button(app, text="Choose Custom Path", command=save_custom_path)
choose_custom_path_button.pack()

# Display custom path (if it exists)
custom_path_label = ttk.Label(app, text=f"Custom Path: {custom_path}")
custom_path_label.pack()

# Option to open the file after creation
open_after_creation = tk.BooleanVar()
open_file_checkbox = ttk.Checkbutton(app, text="Open the file after creation", variable=open_after_creation)
open_file_checkbox.pack()

app.mainloop()
