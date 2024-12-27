import os
import shutil
import json
from pathlib import Path

base_path = Path.home()


class dirSort:

    def __init__(self, directory, settings):
        self.directory = directory
        self.settings = settings


    def is_skola(self, file):
        name = file.lower()
        if len(name) < 6:
            return False

        for i in range(0, 4):
            if not name[i].isalpha():
                return False
        
        for i in range(4, 6):
            if not name[i].isdigit():
                return False
        

    def sort(self, directory):
        self.directory = directory
        print("Sorting: ", self.directory)
        
        for file in os.listdir(directory):
        
            extension = file.split('.')[-1]   
            if extension == file:
                continue

            if self.is_skola(file):
                if self.directory != f'{base_path}/Skola':
                    #shutil.move(f'{self.directory}/{file}', f'{base_path}/Skola')
                    print(f"Moved {file} to Skola")
                    continue
            
            for dir, details in self.settings.items():
                print("extension: ", extension)
                print("details: ", details["Format"])
                if extension in details["Format"]:
                    print(f"{self.directory} == {base_path}/{details['Path']}")
                    if self.directory != f'{base_path}/{details["Path"]}':
                        #shutil.move(f'{self.directory}/{file}', f'{base_path}/{setting}')
                        print(f"Moved {file} to {dir}")
                        break

