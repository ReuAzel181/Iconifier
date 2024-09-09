# Iconifier
### Time Killer Project
Folder Iconifier is a Python application designed to simplify the organization of folders by changing their icons based on the contents of the folder. This tool is particularly useful for users who compile tutorials and tips into folders but struggle with identifying their contents quickly. By using the first image inside a folder to set the folder icon, users can easily distinguish between folders at a glance. The application also displays a random fun fact upon completion.

## Features
  - Create Multi-Size Icons: Convert images into .ico files with multiple sizes.
  - Apply Icons to Folders: Easily assign custom icons to folders.
  - Random Fun Facts: Get a fun fact displayed in green text once processing is complete.
    
## Requirements
  - Python: 3.11 or later
  - Python Packages:
    - Pillow (for image processing)
    - ttkthemes (for enhanced GUI themes)


## Install the required packages using pip:
bash
Copy code
pip install pillow ttkthemes

# Usage
**1. Launch the Application:**
Execute iconifier.py to start the GUI application.

**2. Select Folder:**
Click the "Browse" button to choose the folder containing images for the icons.

**3. Start Processing:**
Click the "Start Processing" button to apply icons to folders. The progress will be shown, and the process will complete with a notification.

**4. View Random Fact:**
After processing, a random fun fact will be displayed in green text in the log area.

<img src="https://raw.githubusercontent.com/ReuAzel181/Iconifier/023fc56737119410a4db4152bb24d2905926b287/rm_imgs/start.png" alt="UI" width="300"/>
<img src="https://raw.githubusercontent.com/ReuAzel181/Iconifier/023fc56737119410a4db4152bb24d2905926b287/rm_imgs/done.png" alt="UI" width="300"/>

![UI](https://raw.githubusercontent.com/ReuAzel181/Iconifier/023fc56737119410a4db4152bb24d2905926b287/rm_imgs/into.png)

## Executable
For those who want the executable, go into the dist folder and download iconifier.exe. Note: The icon might take a while to load. If no icon is applied, rerun the program. Also, ensure that the main file path specified is the folder containing the images, not just the images themselves.

## Notes
  - Ensure the script is run from the directory where it is located, or specify the correct path to the script file.
  - Verify that you have the necessary permissions to modify folders and create files on your system.

## Troubleshooting
For issues, refer to the iconifier.log file for detailed error information.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests. We welcome any improvements or bug fixes!

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or feedback, please reach out to:

Author: **ReuAzel181**

Email: **reyuasel@gmail.com**

Thank you for checking out the Iconifier project!

