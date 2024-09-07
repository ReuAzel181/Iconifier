import os
from PIL import Image
import shutil

def create_multi_size_icon(input_image_path, output_icon_path):
    """
    Create a multi-size .ico file from an input image.
    """
    img = Image.open(input_image_path)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    # Ensure that the image is square (required for .ico files)
    if img.width != img.height:
        img = img.resize((img.width, img.width))  # Resize to make it square
    
    img.save(output_icon_path, format='ICO', sizes=icon_sizes)

def apply_folder_icon(folder_path, icon_path):
    """
    Apply the specified .ico file as the icon for the folder.
    """
    desktop_ini_path = os.path.join(folder_path, 'desktop.ini')
    icon_resource_line = f'IconResource={icon_path},0\n'

    # Check if desktop.ini already contains the correct configuration
    if os.path.exists(desktop_ini_path):
        with open(desktop_ini_path, 'r') as f:
            contents = f.read()
            if icon_resource_line in contents:
                # Icon already applied; no further action needed
                return True

    try:
        with open(desktop_ini_path, 'w') as f:
            f.write('[.ShellClassInfo]\n')
            f.write(icon_resource_line)

        # Ensure desktop.ini is hidden and system file
        os.system(f'attrib +h +s "{desktop_ini_path}"')
        os.system(f'attrib +r "{folder_path}"')

        return True

    except PermissionError:
        return False

def ensure_folder_exists(folder_path):
    """
    Ensure the folder exists, creating it if necessary.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def process_folder(folder_path):
    """
    Process each folder to apply an icon if necessary.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            first_image_path = os.path.join(folder_path, file_name)
            icon_image_copy = os.path.join(folder_path, 'folder_icon_copy.png')
            shutil.copy(first_image_path, icon_image_copy)

            icon_path = os.path.join(folder_path, 'folder_icon.ico')
            create_multi_size_icon(icon_image_copy, icon_path)
            os.remove(icon_image_copy)

            return apply_folder_icon(folder_path, icon_path)

parent_folder = "E:/Modules/Progamming Principles - Copy"

# Counters for logging
already_applied_count = 0
error_count = 0

# Loop through each subfolder in the parent folder
for folder_name in os.listdir(parent_folder):
    folder_path = os.path.join(parent_folder, folder_name)

    if os.path.isdir(folder_path):
        if process_folder(folder_path):
            already_applied_count += 1
        else:
            error_count += 1

# Print summary of results
print(f"Number of folders with icon already applied: {already_applied_count}")
print(f"Number of folders with errors: {error_count}")
