import os
from pathlib import Path



# Exceptions parent for specific handling
class ContextError(Exception):
    pass

# Raised when cwd is set outside the root,
# or linked outside root directory
class ContextPermissionError(ContextError):
    pass

# Context is used by the event handler to keep
# account of the currently open file or folder
class ContextManager:

    def __init__(self, root: (str | Path), cwd: (str | Path) = None):
        if not cwd: cwd = root

        self.root = root if type(root) is Path else Path(root)
        self.root = self.root.resolve(strict=False)
        self.cwd = cwd if type(cwd) is Path else Path(cwd)
        self.cwd = self.cwd.resolve(strict=False)

        if not self.cwd.exists():
            raise ContextError(f"Path does not exist: {self.cwd}")

        if not self.root.exists():
            raise ContextError(f"Root does not exist: {self.root}")

        if not (self.root in self.cwd.parents or self.root == self.cwd):
            raise ContextPermissionError(f"Context outside of root folder")

    def set(self, target_path: (Path, str)):
        # String type is needed by the LLM
        if type(target_path) is str: target_path = Path(target_path)
        target_path = target_path.resolve(strict=False)

        # Check if new path exists
        if not target_path.exists():
            raise ContextError(f"Target path does not exist: {target_path}")
        if not (self.root in target_path.parents or self.root == target_path):
            raise ContextPermissionError(f"Context outside of root folder")
        self.cwd = target_path

    def get(self, abs=False) -> Path:
        relative_path = self.cwd.relative_to(self.root)
        return self.cwd.absolute() if abs else relative_path

    def get_root(self) -> Path:
        return self.root

    def set_root(self, root: (str, Path)):
        # Change root only if it is valid.
        root = root if type(root) is Path else Path(root)

        if not root.exists():
            raise ContextError(f"Root does not exist: {self.root}")
        self.root = root.resolve(strict=True)

        if not (self.root in self.cwd.parents or self.root == self.cwd):
            self.cwd = self.root