import os
import shutil
import json
from pathlib import Path

base_path = Path.home()

DEBUG = True

class dirSort:

    def __init__(self, directory: str, settings: dict):
        self.directory = directory
        self.settings = settings


    def sort(self, directory: str):
        self.directory = directory

        if DEBUG:
            print("Sorting: ", self.directory)
        
        for file in os.listdir(directory):
            if file.startswith('.'):
                continue
            
            if DEBUG: print(f"Checking {file}")
        
            extension = file.split('.')[-1]   
            if extension == file:
                continue


            
            for dir, details in self.settings.items():
                for keyword in details["Keywords"]:
                    if keyword.lower() in file.lower():
                        if DEBUG:
                            print(f"{self.directory} == {base_path}/{details['Path']}")
                        if self.directory != f'{base_path}/{details["Path"]}':
                            if DEBUG:
                                print(f"Moving {file} to {dir}")
                            else:
                                shutil.move(f'{self.directory}/{file}', f'{base_path}/{details["Path"]}')
                            break

                if extension in details["Format"]:
                    if DEBUG:
                        print(f"{self.directory} == {base_path}/{details['Path']}")
                    if self.directory != f'{base_path}/{details["Path"]}':
                        if DEBUG:
                            print(f"Moving {file} to {dir}")
                        else:
                            shutil.move(f'{self.directory}/{file}', f'{base_path}/{details["Path"]}')
                        break

