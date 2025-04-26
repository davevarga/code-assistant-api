import os
from typing import List
from smolagents import tool
from llm import context


@tool
def find_file(filename: str) -> List[str]:
    """
    Finds all instances of a filename within the project
    and returns a list of relative paths from the root
    Args:
        filename (str): The filename to search for
    Returns:
        List[str]: A list of relative paths from the root
    """
    root_dir = context.get_root()

    matches: List[str] = []
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if filename in files:
            matches.append(os.path.join(root, filename))

    content = [os.path.join(root_dir, match) for match in matches]
    content = [path.replace("\\", "/") for path in content]
    return content