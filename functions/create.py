import os
from llm import context, check_syntax
from smolagents import tool


@tool
def create_file_or_directory(name: str) -> str:
    """
    It creates either a file or directory in the current directory.
    A file is created if an extension is provided. Otherwise, it
    creates a new directory.
    Args:
        name: Name of the file or directory.
    Returns:
        The path of the created file or directory.
    """
    curr_dir = context.get()
    path = os.path.join(curr_dir, name)

    # Check if is already created
    if os.path.exists(path):
        return path

    # Normalize the path to avoid issues with trailing slashes
    # Extract the base name and check for a file extension
    path = os.path.normpath(path)
    _, extension = os.path.splitext(path)

    if extension:
        file = open(path, "w")
        file.write("")
    else:
        os.makedirs(path, exist_ok=True)

    # Return with the path of the created file.
    return path