import os
from smolagents import tool
from utils import context


@tool
def open_file_or_directory(name: str) -> str:
    """
    Lets you navigate in the working directory, or open files for editing.
    To go back use the command with the argument: ../
    Args:
        name (str): Relative path of the file or directory.
    Returns:
        str: If the procedure was successful.
    """
    try:
        context.set(name)
        return f"Successfully opened {context.get()}"
    except FileNotFoundError:
        return f"File does not exist in {context.get()}"
    except PermissionError:
        return f"{name} permission denied"