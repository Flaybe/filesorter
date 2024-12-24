import os
import shutil

class dirSort:

    def __init__(self, directory):
        self.directory = directory
        self.files = os.listdir(directory)


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
        

    def sort(self):
        for file in self.files:

            extension = file.split('.')[-1]
            print("Extension: ", extension)
            
            if self.is_skola(file):
                if self.directory != '/Users/mateo/Skola':
                    shutil.move(f'{self.directory}/{file}', '/Users/mateo/Skola')
                    continue

            match extension:
                case 'jpg' | 'jpeg' | 'png' | 'gif':
                    if self.directory != '/Users/mateo/Pictures':
                        shutil.move(f'{self.directory}/{file}', '/Users/mateo/Pictures')
                        print(f"Moved {file} to Pictures")
                        continue
                case 'doc' | 'docx' |  'pdf':
                    if self.directory != '/Users/mateo/Documents':
                        shutil.move(f'{self.directory}/{file}', '/Users/mateo/Documents')
                        print(f"Moved {file} to Documents")
                        continue
                case 'mp3' | 'wav':
                    if self.directory != '/Users/mateo/Music':
                        shutil.move(f'{self.directory}/{file}', '/Users/mateo/Music')
                        print(f"Moved {file} to Music")
                        continue
                case 'mp4' | 'avi':
                    if self.directory != '/Users/mateo/Music':
                        shutil.move(f'{self.directory}/{file}', '/Users/mateo/Videos')
                        print(f"Moved {file} to Videos")
                        continue
                case 'zip' | 'rar':
                    if self.directory != '/Users/mateo/Downloads':
                        shutil.move(f'{self.directory}/{file}', '/Users/mateo/Downloads')
                        print(f"Moved {file} to Downloads")
                        continue
                case _:
                    print(f"Unknown file type: {file}")
                    continue    

