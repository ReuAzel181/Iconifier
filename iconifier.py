import os
import shutil
from PIL import Image
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from ttkthemes import ThemedTk
from threading import Thread
import time

# Set up logging
logging.basicConfig(filename='iconifier.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_multi_size_icon(input_image_path, output_icon_path):
    try:
        img = Image.open(input_image_path)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        # Resize image to be square if necessary
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
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            first_image_path = os.path.join(folder_path, file_name)
            icon_image_copy = os.path.join(folder_path, 'folder_icon_copy.png')
            shutil.copy(first_image_path, icon_image_copy)

            icon_path = os.path.join(folder_path, 'folder_icon.ico')
            create_multi_size_icon(icon_image_copy, icon_path)
            os.remove(icon_image_copy)

            return apply_folder_icon(folder_path, icon_path)

def process_folders():
    folder_path = folder_path_var.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path")
        return

    progress_bar['value'] = 0
    log_output.delete(1.0, tk.END)
    root.update_idletasks()

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

            progress_bar['value'] = (i + 1) / total_folders * 100
            status_label.config(text=f"Processing folder: {folder_name}")
            root.update_idletasks()
            time.sleep(0.1)  # Simulate processing delay

    result_text = (
        f"Number of folders with icon already applied: {already_applied_count}\n"
        f"Number of folders with errors: {error_count}"
    )
    log_output.insert(tk.END, result_text + '\n')
    log_output.yview(tk.END)
    status_label.config(text="Processing complete!")

def start_process():
    process_thread = Thread(target=process_folders)
    process_thread.start()

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)

# Set up the GUI with a modern theme
root = ThemedTk(theme="breeze")  # You can choose other themes like "arc", "radiance", etc.
root.title("Folder Iconifier")
root.geometry("600x400")

# Frame for the input controls
frame_controls = ttk.Frame(root, padding="10")
frame_controls.pack(fill=tk.X)

# Folder Path Input
ttk.Label(frame_controls, text="Select Folder:").pack(pady=5, anchor=tk.W)
folder_path_var = tk.StringVar()
ttk.Entry(frame_controls, textvariable=folder_path_var, width=50).pack(pady=5, side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(frame_controls, text="Browse", command=browse_folder).pack(pady=5, side=tk.RIGHT)

# Start Button
ttk.Button(root, text="Start Processing", command=start_process).pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

# Status Label
status_label = ttk.Label(root, text="Please select a folder and start processing")
status_label.pack(pady=5)

# Log Output
frame_log = ttk.Frame(root, padding="10")
frame_log.pack(fill=tk.BOTH, expand=True)

log_output = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, height=10)
log_output.pack(fill=tk.BOTH, expand=True)

root.mainloop()
