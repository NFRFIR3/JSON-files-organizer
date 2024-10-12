import os
import shutil
import re
import ctypes

# Step 1: Define paths
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")  # Your Downloads folder
destination_folder = os.path.join(download_folder, "Full Json Files")  # The new folder for JSON files

# Step 2: Check if the 'Full Json Files' folder already exists
if os.path.exists(destination_folder):
    print("The 'Full Json Files' folder already exists.")
    action = input("Type 1 to reorganize the JSON files, or type 2 to remove all JSON files from the folder and put them back in the Downloads folder: ").strip()

    if action == '1':
        # Reorganize the JSON files inside the 'Full Json Files' folder
        print("Reorganizing the JSON files into the 'Full Json Files' folder...")

        # Step 3: Create a dictionary to group similar files based on their base names
        json_files = {}

        # Regular expression to match the base part of filenames (ignores numbers and index suffixes like (1), (2))
        pattern = re.compile(r"([a-zA-Z_]+)(\d+)?(\s\(\d+\))?")

        # Step 4: Get all .json files from the Downloads folder and group them
        for filename in os.listdir(download_folder):
            if filename.endswith(".json"):
                match = pattern.match(os.path.splitext(filename)[0])
                if match:
                    base_name = match.group(1)  # The base part of the name, ignoring numbers and indexes
                    if base_name not in json_files:
                        json_files[base_name] = [filename]
                    else:
                        json_files[base_name].append(filename)

        # Step 5: Organize the files into folders
        folders_created = []

        for base_name, files in json_files.items():
            if len(files) > 1:
                # If there are multiple similar files, create a folder for them
                base_folder = os.path.join(destination_folder, f"{base_name} Jsons")
                if not os.path.exists(base_folder):
                    os.makedirs(base_folder)
                folders_created.append(base_folder)

                for file in files:
                    source_path = os.path.join(download_folder, file)
                    destination_path = os.path.join(base_folder, file)
                    shutil.move(source_path, destination_path)

            else:
                # If there's only one file, create a folder just for this file
                single_folder = os.path.join(destination_folder, base_name)
                if not os.path.exists(single_folder):
                    os.makedirs(single_folder)
                folders_created.append(single_folder)

                source_path = os.path.join(download_folder, files[0])
                destination_path = os.path.join(single_folder, files[0])
                shutil.move(source_path, destination_path)

        # Step 6: Display a Windows message box with the results
        if folders_created:
            folder_list = "\n".join(f"{folder}" for folder in folders_created)
            message = f"All JSON files have been reorganized into the following folders:\n\n{folder_list}"
            ctypes.windll.user32.MessageBoxW(0, message, "JSON Files Reorganized", 0x40 | 0x1)

    elif action == '2':
        # Move all the JSON files back to the Downloads folder
        print("Removing all JSON files from 'Full Json Files' and placing them back in the Downloads folder...")

        # Traverse the 'Full Json Files' folder to move the files back to Downloads
        for root, dirs, files in os.walk(destination_folder):
            for file in files:
                if file.endswith(".json"):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(download_folder, file)
                    shutil.move(source_path, destination_path)
                    print(f"Moved: {file} back to Downloads folder.")

        # Optionally, remove empty folders after moving files
        for root, dirs, files in os.walk(destination_folder, topdown=False):
            if not os.listdir(root):  # If folder is empty
                os.rmdir(root)

        # Notify the user
        ctypes.windll.user32.MessageBoxW(0, "All JSON files have been moved back to the Downloads folder.", "JSON Files Removed", 0x40 | 0x1)

    else:
        print("Invalid option selected.")

else:
    # If the 'Full Json Files' folder doesn't exist, create it and organize the files
    print("The 'Full Json Files' folder does not exist. Creating and organizing files now...")

    # Step 3: Create 'Full Json Files' folder
    os.makedirs(destination_folder)

    # Step 4: Create a dictionary to group similar files based on their base names
    json_files = {}

    # Regular expression to match the base part of filenames (ignores numbers and index suffixes like (1), (2))
    pattern = re.compile(r"([a-zA-Z_]+)(\d+)?(\s\(\d+\))?")

    # Step 5: Get all .json files from the Downloads folder and group them
    for filename in os.listdir(download_folder):
        if filename.endswith(".json"):
            match = pattern.match(os.path.splitext(filename)[0])
            if match:
                base_name = match.group(1)  # The base part of the name, ignoring numbers and indexes
                if base_name not in json_files:
                    json_files[base_name] = [filename]
                else:
                    json_files[base_name].append(filename)

    # Step 6: Organize the files into folders
    folders_created = []

    for base_name, files in json_files.items():
        if len(files) > 1:
            # If there are multiple similar files, create a folder for them
            base_folder = os.path.join(destination_folder, f"{base_name} Jsons")
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)
            folders_created.append(base_folder)

            for file in files:
                source_path = os.path.join(download_folder, file)
                destination_path = os.path.join(base_folder, file)
                shutil.move(source_path, destination_path)

        else:
            # If there's only one file, create a folder just for this file
            single_folder = os.path.join(destination_folder, base_name)
            if not os.path.exists(single_folder):
                os.makedirs(single_folder)
            folders_created.append(single_folder)

            source_path = os.path.join(download_folder, files[0])
            destination_path = os.path.join(single_folder, files[0])
            shutil.move(source_path, destination_path)

    # Step 7: Display a Windows message box with the results
    if folders_created:
        folder_list = "\n".join(f"{folder}" for folder in folders_created)
        message = f"All JSON files have been organized into the Full Json Files folder " #\n\n{folder_list} -- test ignore
        ctypes.windll.user32.MessageBoxW(0, message, "JSON Files Organized", 0x40 | 0x1)
