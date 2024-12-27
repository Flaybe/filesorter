import os
import shutil
import json
from pathlib import Path

base_path = Path.home()

DEBUG = False

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

        if DEBUG:
            print("Sorting: ", self.directory)
        
        for file in os.listdir(directory):
        
            extension = file.split('.')[-1]   
            if extension == file:
                continue

            if self.is_skola(file):
                if self.directory != f'{base_path}/Skola':
                    if DEBUG:
                        print(f"Moving {file} to Skola")
                    else:
                        shutil.move(f'{self.directory}/{file}', f'{base_path}/Skola')
                    continue
            
            for dir, details in self.settings.items():
                if extension in details["Format"]:
                    print(f"{self.directory} == {base_path}/{details['Path']}")
                    if self.directory != f'{base_path}/{details["Path"]}':
                        if DEBUG:
                            print(f"Moving {file} to {dir}")
                        else:
                            shutil.move(f'{self.directory}/{file}', f'{base_path}/{details["Path"]}')
                        break

