import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from RadioUI import RadioUI
from Settings import SettingsWindow

# Function to create second window for SO2R or 2BSIQ
second_window = None

def create_second_window():
    global second_window
    if second_window is None or not second_window.winfo_exists():
        second_ui = RadioUI("Radio 2", contest="ARRL10")
        second_window = second_ui.get_window()

# Function to close second window if it exists

def close_second_window():
    global second_window
    if second_window is not None and second_window.winfo_exists():
        second_window.destroy()

# Main application window
radios = [RadioUI("Radio 1", contest="ARRL10")]
root = radios[0].get_window()

# Create a menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add 'File' menu with 'Settings' option
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Settings", command=lambda: SettingsWindow(root, create_second_window, close_second_window))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()
