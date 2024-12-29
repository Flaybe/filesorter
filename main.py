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


    def sort(self, directory: str) -> list[tuple[str, str]]:
        moves = []
        self.directory = directory

        if DEBUG:
            print("Sorting: ", self.directory)
        
        # Remove all hidden files
        for file in os.listdir(directory):
            if file.startswith('.'):
                continue
            
            if DEBUG: print(f"Checking {file}")

            extension = file.split('.')[-1] 

            # Check if the file is a directory
            if extension == file:
                continue
            
            for dir, details in self.settings.items():
                # Check for keywords
                for keyword in details["Keywords"]:
                    if keyword.lower() in file.lower():
                        if DEBUG:
                            print(f"{self.directory} == {base_path}/{details['Path']}")
                        if self.directory != f'{base_path}/{details["Path"]}':
                            moves.append((f'{self.directory}/{file}', f'{base_path}/{details["Path"]}'))
                            if DEBUG:
                                print(f"Moving {file} to {dir}")
                            break
                
                #Check for format
                if extension in details["Format"]:
                    if DEBUG:
                        print(f"{self.directory} == {base_path}/{details['Path']}")
                    if self.directory != f'{base_path}/{details["Path"]}':
                        moves.append((f'{self.directory}/{file}', f'{base_path}/{details["Path"]}'))
                        if DEBUG:
                            print(f"Moving {file} to {dir}")
                        else:
                            shutil.move(f'{self.directory}/{file}', f'{base_path}/{details["Path"]}')
                        break
        return moves

