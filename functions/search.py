from typing import List

from smolagents import tool
from llm import context
import os

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


@tool
def search_dir_for_matches(template: str) -> List[str]:
    """
    Starts a search for occurrences of the given string. It searches through any
    files and subdirectories starting with the current working directory or file.
    Useful when searching for a function or a class in a project.
    Args:
        template (str): The string to search for.
    Returns:
        List[str]: A list of all occurrences of the template. Consists of the file
        path, line number, and a snippet of the code, separated by dashes
    """

    current_path = context.get_abs()
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

    content = [
        (f"./{os.path.relpath(occurrence['path'], current_path)}"
         f"-{occurrence["line"]}"
         f"-{occurrence['snippet']}")
        for occurrence in occurrences
    ]
    return content