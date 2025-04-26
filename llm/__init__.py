import os
import ast

# Context is used by the event handler to keep
# account of the currently open file or folder

class ContextHandler:

    def __init__(self, root, current_path=None):
        self.root = root
        if not os.path.isdir(self.root):
            raise ValueError(f"Root must be an existing directory: {self.root}")
        self.current_path = current_path if current_path else self.root

    def set(self, target_path: os.PathLike):
        # Resolve the full absolute path
        new_path = os.path.normpath(os.path.join(self.current_path, target_path))

        # Ensure we do not leave the root directory
        # if not os.path.commonpath([self.root, new_path]).startswith(self.root):
        #     raise PermissionError("Access denied: attempted to move outside the root directory.")

        # Check if new path exists
        if not os.path.exists(new_path):
            raise FileNotFoundError(f"Target path does not exist: {target_path}")

        self.current_path = new_path

    def get(self):
        return os.path.relpath(self.current_path, self.root)

    def get_abs(self):
        return self.current_path

    def get_root(self):
        return self.root

    def set_root(self, root_directory):
        self.root = root_directory
        self.current_path = root_directory


def check_syntax(code: str):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return [f"Invalid syntax {e}"]


# Instantiation takes place now, so that certain
# function calling tools can manipulate the context.
context = ContextHandler('D:/Projects/code-assistant-api')