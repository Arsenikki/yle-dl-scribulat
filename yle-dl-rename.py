import glob
import os
import pathlib
import shutil

# Inputs

# Dry run will print the changes without actually renaming the files
# Note dry run only works with rename_file function
dry_run = False
fix_episode_format = True

# Globals. DO NOT TOUCH PERKELE
count = 1
failedFiles = []
previous_season = "S01"

# Specify the directory containing the files
input_dir = "./downloads"
output_dir = "./processed_episodes"

def fix_episode_formats(old_filename):
    global count
    global previous_season

    print("-------------------")
    parts = filename.split('_')
    if len(parts) == 3:
        episodeId = parts[1].strip(".")
    else:
        print(f"Failed to fix episode format for {filename}")
        failedFiles.append(filename)
        return
    
    parts = episodeId.split('E')
    current_season = parts[0]
    if current_season != previous_season:
        count = 1
        previous_season = current_season

    new_episode_id = f"{current_season}E{count:02d}"
    count += 1

    old_path = os.path.join(output_dir, old_filename)
    new_filename = filename.replace(episodeId, new_episode_id).replace("_", "")
    
    new_path = os.path.join(output_dir, new_filename)
    if not dry_run:
        # Move and rename files
        os.rename(old_path, new_path)
    

def splitFilename(old_filename):
    # Split filename and file extension
    baseFileName = os.path.splitext(old_filename)[0]

    # Strip the timestamp from the filename
    baseFileName = baseFileName[:-17]
    # Split and reorder the parts of the filename
    return baseFileName.split(":")

def rename_file(old_filename):
    extension = os.path.splitext(old_filename)[1]
    filenameParts = splitFilename(old_filename)
    if len(filenameParts) == 3:
        new_filename = f"{filenameParts[0]}_{filenameParts[2]}_{filenameParts[1]}{extension}"
    else:
        print(f"Failed to rename {old_filename}")
        failedFiles.append(old_filename)
        return

    # Replace spaces with periods
    new_filename = new_filename.replace(" ", ".")

    print(f"Renaming {filename} to {new_filename}")
    # Create the full file paths
    old_path = os.path.join(input_dir, old_filename)
    new_path = os.path.join(output_dir, new_filename)
    print(f"Input: {old_path}")
    print(f"Output: {new_path}")
    if not dry_run:
        # Move and rename files
        shutil.copy(old_path, new_path)


# Create the output directory if it doesn't exist
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

for filename in os.listdir(input_dir):
    # Call the function to rename the files in the directory
    rename_file(filename)

# Read each file in the OUTPUT directory in sorted order
if fix_episode_format and not dry_run:
    for filename in sorted(glob.glob(output_dir + "/*")):
        if failedFiles.count(filename) > 0:
            break
        # Fix Episode IDs to standard format where episode numbers are reset per season
        # i.e. S05E02 instead of S05E55
        filename = os.path.basename(filename)
        fix_episode_formats(filename)

print("-------------------")
print("-------------------")
print("-------------------")

if len(failedFiles) > 0:
    print("Something went wrong!")
    print(f"Following files caused issues in '{output_dir}':")
    for file in failedFiles:
        print(file)
    exit(1)
if dry_run:
    print("Dry run completed successfully! Change 'dry_run' to False to rename the files.")
else:
    print("My work here is done! Jahuu!")
