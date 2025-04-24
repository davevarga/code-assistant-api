import os
from smolagents import tool
from llm import context


@tool
def open_file_or_directory(name: str) -> bool:
    """
    Lets you navigate in the working directory, or open files for editing.
    To go back use the command with the argument: ../
    Args:
        name: Relative path of the file or directory.
    Returns:
        bool: If the procedure was successful.
    """
    try:
        context.set(name)
        return True
    except FileNotFoundError:
        return False
    except PermissionError:
        return False