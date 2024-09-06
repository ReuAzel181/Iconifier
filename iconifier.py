import os
from PIL import Image
import shutil

def create_multi_size_icon(input_image_path, output_icon_path):
    """
    Create a multi-size .ico file from an input image.
    The icon will contain sizes 16x16, 32x32, 48x48, 64x64, 128x128, and 256x256.
    """
    img = Image.open(input_image_path)

    # Define the sizes we want in the .ico file
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    # Save the image in .ico format with multiple sizes
    img.save(output_icon_path, format='ICO', sizes=icon_sizes)

def apply_folder_icon(folder_path, icon_path, max_retries=3):
    """
    Apply the specified .ico file as the icon for the folder.
    Retry up to `max_retries` times if PermissionError occurs.
    """
    desktop_ini_path = os.path.join(folder_path, 'desktop.ini')

    # Check if the desktop.ini file already exists and contains the correct icon path
    if os.path.exists(desktop_ini_path):
        with open(desktop_ini_path, 'r') as f:
            content = f.read()
            if f'IconResource={icon_path}' in content:
                print(f"Icon already applied for folder: {folder_path}")
                return  # Skip if the icon is already applied

    # Retry logic
    retries = 0
    success = False
    while retries < max_retries and not success:
        try:
            # Write desktop.ini file to assign the folder icon
            with open(desktop_ini_path, 'w') as f:
                f.write('[.ShellClassInfo]\n')
                f.write(f'IconResource={icon_path},0\n')

            # Set the desktop.ini file as hidden and a system file
            os.system(f'attrib +h +s "{desktop_ini_path}"')

            # Set the folder to read-only (necessary for custom icons)
            os.system(f'attrib +r "{folder_path}"')

            print(f"Icon successfully applied to folder: {folder_path}")
            success = True  # If no error occurs, we break out of the retry loop
        
        except PermissionError:
            retries += 1
            print(f"Permission denied: Unable to write to {desktop_ini_path}. Retry {retries}/{max_retries}...")

            # Try removing the read-only attribute and retrying
            os.system(f'attrib -r "{folder_path}"')

    if not success:
        print(f"Failed to apply icon to folder: {folder_path} after {max_retries} retries.")

def ensure_folder_exists(folder_path):
    """
    Ensure the folder exists, creating it if necessary.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

# Define the parent folder containing all subfolders
parent_folder = "E:/Modules/Progamming Principles - Copy"

# Loop through each subfolder in the parent folder
for folder_name in os.listdir(parent_folder):
    folder_path = os.path.join(parent_folder, folder_name)

    # Ensure the folder exists
    ensure_folder_exists(folder_path)

    # Check if it's a folder
    if os.path.isdir(folder_path):
        # Find the first image file in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                first_image_path = os.path.join(folder_path, file_name)

                # Create a duplicate of the first image for icon conversion
                icon_image_copy = os.path.join(folder_path, 'folder_icon_copy.png')
                shutil.copy(first_image_path, icon_image_copy)

                # Convert the duplicate image to a multi-size .ico format
                icon_path = os.path.join(folder_path, 'folder_icon.ico')
                create_multi_size_icon(icon_image_copy, icon_path)

                # Delete the duplicate image after conversion
                os.remove(icon_image_copy)

                # Apply the generated icon to the folder, with retry limit
                apply_folder_icon(folder_path, icon_path)

                break  # Stop after processing the first image in the folder
