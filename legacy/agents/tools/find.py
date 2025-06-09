import os
from typing import List
from smolagents import Tool
from utils import ContextManager


class FindTool(Tool):
    name = "find_file"
    description = """Finds all instances of a filename within the project
        and returns a list of relative paths from the root"""
    inputs = {
        "filename": {
            "type": "string",
            "description": "The filename to search for"
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, filename: str) -> str:
        root_dir = self.context.get_root()
        matches: List[str] = []
        for root, dirs, files in os.walk(root_dir):
            # Modify dirs in-place to skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if filename in files:
                matches.append(os.path.join(root, filename))
                matches.append(os.path.join(root, filename))

        content = [os.path.join(root_dir, match) for match in matches]
        content = [path.replace("\\", "/") for path in content]
        content = [os.path.relpath(path, root_dir) for path in content]
        if not content: return f'No files found with name {filename}'
        return '\n'.join(content)