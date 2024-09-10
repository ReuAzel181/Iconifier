import os
import sys
import shutil
from PIL import Image, ImageTk
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from ttkthemes import ThemedTk
from tkinter import font 
from threading import Thread
import random
import subprocess

# Set up logging
logging.basicConfig(filename='iconifier.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_multi_size_icon(input_image_path, output_icon_path):
    try:
        img = Image.open(input_image_path)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        if img.width != img.height:
            img = img.resize((img.width, img.width))
        
        img.save(output_icon_path, format='ICO', sizes=icon_sizes)
        logging.info(f"Icon created: {output_icon_path}")
    except Exception as e:
        logging.error(f"Failed to create icon: {e}")

def apply_folder_icon(folder_path, icon_path):
    desktop_ini_path = os.path.join(folder_path, 'desktop.ini')
    icon_resource_line = f'IconResource={icon_path},0\n'

    try:
        if os.path.exists(desktop_ini_path):
            with open(desktop_ini_path, 'r') as f:
                contents = f.read()
                if icon_resource_line in contents:
                    logging.info(f"Icon already applied to folder: {folder_path}")
                    return True

        with open(desktop_ini_path, 'w') as f:
            f.write('[.ShellClassInfo]\n')
            f.write(icon_resource_line)

        os.system(f'attrib +h +s "{desktop_ini_path}"')
        os.system(f'attrib +r "{folder_path}"')

        logging.info(f"Icon applied to folder: {folder_path}")
        return True

    except PermissionError as e:
        logging.error(f"Permission error applying icon to folder {folder_path}: {e}")
        return False

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def process_folder(folder_path):
    print(f"Processing folder: {folder_path}")  # Debugging statement
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            first_image_path = os.path.join(folder_path, file_name)
            icon_image_copy = os.path.join(folder_path, 'folder_icon_copy.png')
            shutil.copy(first_image_path, icon_image_copy)

            icon_path = os.path.join(folder_path, 'folder_icon.ico')
            create_multi_size_icon(icon_image_copy, icon_path)
            os.remove(icon_image_copy)

            result = apply_folder_icon(folder_path, icon_path)
            print(f"Icon application result for {folder_path}: {result}")  # Debugging statement

            return result

def process_folders():
    folder_path = folder_path_var.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path")
        return

    # Disable the Entry widget while processing
    folder_entry.config(state=tk.DISABLED)

    progress_bar['value'] = 0
    log_output.config(state=tk.NORMAL)  # Enable editing to insert text
    log_output.delete(1.0, tk.END)
    
    already_applied_count = 0
    error_count = 0
    total_folders = len([f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))])

    for i, folder_name in enumerate(os.listdir(folder_path)):
        subfolder_path = os.path.join(folder_path, folder_name)
        if os.path.isdir(subfolder_path):
            if process_folder(subfolder_path):
                already_applied_count += 1
            else:
                error_count += 1

            # Update progress bar and UI only after every few folders to avoid too frequent updates
            if i % 10 == 0 or i == total_folders - 1:  # Update every 10 folders or on the last one
                progress_bar['value'] = (i + 1) / total_folders * 100
                status_label.config(text=f"Processing folder: {folder_name}")
                root.update_idletasks()

    # List of random facts
    facts = [
        "Honey never spoils.",
        "A group of flamingos is called a 'flamboyance.'",
        "The heart of a shrimp is located in its head.",
        "Bananas are berries, but strawberries aren't.",
        "The Eiffel Tower can be 15 cm taller during the summer.",
        "An octopus has three hearts.",
        "A day on Venus is longer than a year on Venus.",
        "Wombat poop is cube-shaped.",
        "Sharks have been around longer than trees",
        "A group of cats is called a clowder",
        "The unicorn is Scotland's national animal", 
        "A day on Mercury is equivalent to 59 Earth days", 
        "Octopuses have blue blood", 
        "Honeybees can recognize human faces", 
        "A snail can sleep for three years", 
        "The longest time between two twins being born is 87 days", 
        "Some turtles can breathe through their butts", 
        "The inventor of the Pringles can is now buried in one", 
        "Wombat feces are cube-shaped to prevent them from rolling away", 
        "The world’s largest desert is Antarctica", 
        "An adult human is made up of about 37.2 trillion cells"
    ]
    
    # Pick a random fact
    random_fact = random.choice(facts)
    
    # Build the result text
    result_text = (
        f"Number of folders with icon already applied: {already_applied_count}\n"
        f"Number of folders with errors: {error_count}\n"
        f"Total folders processed: {total_folders}\n\n"
        f"RANDOM FACT: {random_fact}"
    )
    
    # Insert the result text into log_output
    log_output.insert(tk.END, result_text + '\n')
    
    # Determine the start index after "RANDOM FACT: "
    start_index = len(f"Number of folders with icon already applied: {already_applied_count}\n" +
                      f"Number of folders with errors: {error_count}\n" +
                      f"Total folders processed: {total_folders}\n\nRANDOM FACT: ")
    
    # Determine the end index based on the length of random_fact
    end_index = start_index + len(random_fact)
    
    # Convert indices to tk.Text indices
    start_idx = f"1.0 + {start_index} chars"
    end_idx = f"1.0 + {end_index} chars"

    # Define the tag for green text
    log_output.tag_configure("green", foreground="green")

    # Apply the green tag to the random fact part
    log_output.tag_add("green", start_idx, end_idx)
    
    log_output.yview(tk.END)
    status_label.config(text="Processing complete!")

    # Enable the Entry widget and show the "Open Folder" button
    folder_entry.config(state=tk.NORMAL)
    open_folder_button.pack(pady=(5, 10), fill=tk.X)  # Ensure button is packed

    log_output.config(state=tk.DISABLED)  # Make the ScrolledText read-only

def start_process():
    process_thread = Thread(target=process_folders)
    process_thread.start()

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:  # Ensure a folder was selected
        folder_selected = folder_selected.strip()  # Strip any leading/trailing spaces
        folder_path_var.set(folder_selected)
        print(f"Folder path set to: {folder_path_var.get()}")  # Debugging statement

def open_folder():
    folder_path = folder_path_var.get()
    
    if not folder_path:
        print("No folder path set.")  # Debugging statement
        return

    folder_path = folder_path.strip()  # Ensure no leading/trailing spaces
    if os.path.isdir(folder_path):
        print(f"Opening folder path: {folder_path}")  # Debugging statement
        if sys.platform == 'win32':
            # Use os.startfile on Windows (recommended for opening folders)
            try:
                os.startfile(folder_path)
            except Exception as e:
                print(f"Error opening folder on Windows: {e}")  # Debugging statement
        elif sys.platform == 'darwin':  # macOS
            subprocess.Popen(['open', folder_path])
        elif sys.platform == 'linux':  # Linux
            subprocess.Popen(['xdg-open', folder_path])
    else:
        print(f"Invalid folder path: {folder_path}")  # Debugging statement

root = ThemedTk(theme="breeze")  # You can choose other themes like "arc", "radiance", etc.
root.title("Basta SL, WOW!")
root.geometry("600x400")

# Center the window
window_width = 600
window_height = 400

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position x, y
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

frame_controls = ttk.Frame(root, padding="10")
frame_controls.pack(fill=tk.X)

ttk.Label(frame_controls, text="Select Folder:").pack(pady=5, anchor=tk.W)
folder_path_var = tk.StringVar()
folder_entry = ttk.Entry(frame_controls, textvariable=folder_path_var, width=50)
folder_entry.pack(pady=5, side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(frame_controls, text="Browse", command=browse_folder).pack(pady=5, side=tk.RIGHT)

ttk.Button(root, text="Start Processing", command=start_process).pack(pady=(10, 5))

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=(5, 10))

status_label = ttk.Label(root, text="Please select a folder and start processing")
status_label.pack(pady=(5, 10))

frame_log = ttk.Frame(root, padding="10")
frame_log.pack(fill=tk.BOTH, expand=True)

log_output = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, height=7)
log_output.pack(fill=tk.BOTH, expand=True)

# Create and hide the Open Folder button initially
open_folder_button = ttk.Button(root, text="Open Processed Folder", command=open_folder)
open_folder_button.pack(pady=(5, 10), fill=tk.X)  # Ensure button is packed
open_folder_button.pack_forget()  # Hide initially

root.mainloop()
