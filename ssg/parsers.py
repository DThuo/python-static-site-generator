import shutil

from typing import List
from pathlib import Path

import sys
import docutils
from docutils.core import publish_parts
from markdown import markdown
from ssg.content import Content



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
    
    