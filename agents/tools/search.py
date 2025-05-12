from typing import List
from smolagents import tool, Tool
import os

from utils import ContextManager

extensions = ('.py', '.pyi', '.sh', '.bash', '.psi'
              '.toml', '.ini', '.cfg', '.json', '.yaml', '.yml'
              '.md', '.rst', '.txt', '.xml', '.html', '.css', '.js')


def search_file(file_path, query):
    """"""
    results = []
    try:
        with open(file_path, "r", encoding='utf-8', errors='ignore') as file:
            for i, line in enumerate(file, start=1):
                if query in line:
                    results.append({
                        "path": file_path,
                        "line":i,
                        "snippet":line.strip()
                    })
    except Exception:
        # Skip files that can't be read (e.g., binary files or permission errors)
        pass
    return results


class SearchTool(Tool):
    name = "search_dir_for_matches"
    description = """Starts a search for occurrences of the given string. It searches through any
        files and subdirectories starting with the current working directory or file.
        Useful when searching for a function or a class in a project."""
    inputs = {
        "template": {
            "type": "string",
            "description": "The string to search for."
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, template: str) -> str:
        current_path = self.context.get(abs=True)
        occurrences = []
        if os.path.isfile(current_path):
            occurrences += search_file(current_path, template)

        elif os.path.isdir(current_path):
            for root, dirs, files in os.walk(current_path):
                # Modify dirs in-place to skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith(extensions):
                        file_path = os.path.join(root, file)
                        occurrences += search_file(file_path, template)

        content = [f"[Found {len(occurrences)} matches for "
                   f"'{template}' in {self.context.get()} files]"]
        content += [
            (f"./{os.path.relpath(occurrence['path'], current_path)}"
             f" at line {occurrence['line']}:"
             f" '{occurrence['snippet']}'")
            for occurrence in occurrences
        ]
        return '\n'.join(content)