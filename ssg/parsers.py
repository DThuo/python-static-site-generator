import shutil
import sys

from typing import List
from pathlib import Path

from docutils.core import publish_parts
from markdown import markdown
from ssg.content import Content

class Parser:
    base_ext = ".html"
    file_exts: List[str] = []

    def valid_file_exts(self, extensions):
        return file_exts in self.file_exts
    
    def parse(self, path: Path, source: Path, dest: Path):
        raise NotImplementedError
    
    def read(self, path):
        with open(path, "r") as file:
            return file.read() 
        
    def write(self, path, dest, content):
        file_path = dest  / path.with_suffix(self.base_ext).name
        with open(file_path, "w") as file:
            file.write(content)

    def copy(self, path, source, dest):
        shutil.copy2(path, dest / path.relative_to(source))

class ResourceParser(Parser):
    extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    def parse(self, path, source, dest):
        self.copy(path, source, dest)


class MarkdownParser(Parser):
    extensions = [".md", ".markdown"]
    
    def parse(self, path, source, dest):
        content = Content.load(self.read(path))
        html = markdown(content.body)
        sys.stdout.write("\x1b[1;32m{} converted to HTML. Metadata: {}\n".format(path.name, content))
            
class ReStructuredTextParser(Parser): 
    extensions =[".rst"]
    
    def parse(self, path, source, dest):
        content = Content.load(self.read(path))
        html = markdown(content.body)
        sys.stdout.write("\x1b[1;32m{} converted to HTML. Metadata: {}\n".format(path.name, content))
    
    