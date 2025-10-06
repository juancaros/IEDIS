import os
import datetime

def get_files_creation_dates(folder_path):
    files_creation_dates = {}
    
    # List all files in the given folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Get the creation time
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.datetime.fromtimestamp(creation_time)
            files_creation_dates[filename] = creation_date
    
    return files_creation_dates

folder_path = 'C:/Users/a5368/OneDrive/Escritorio/tarea daniel/sust5/2023/2023/'

files_creation_dates = get_files_creation_dates(folder_path)

for filename, creation_date in files_creation_dates.items():
    print(f"File: {filename}, Created on: {creation_date}")

# You can also save this information to a CSV file if needed
import csv

output_csv = 'file_creation_dates.csv'
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Creation Date"])
    for filename, creation_date in files_creation_dates.items():
        writer.writerow([filename, creation_date])