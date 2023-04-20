import shutil

from typing import List
from pathlib import Path



class Parser:
    ext = ".html"
    extensions: List[str] = []

    def valid_extension(self, extensions):
        return extensions in self.extensions
    
    def parse(self, path: Path, source: Path, dest: Path):
        raise NotImplementedError
    
    def read(self, path):
        with open(path) as file:
            return file.read() 
        
    def write(self, path, dest, content):
        full_path = self.dest  / path.with_suffix(self.ext).name
        with open(full_path) as file:
            file.write(content)

    def copy(self, path, source, dest):
        shutil.copy2(path, dest / path.relative_to(source))

class ResourceParser(Parser):
    extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    def parse(self, path, source, dest):
        self.copy(path, source, dest)

        