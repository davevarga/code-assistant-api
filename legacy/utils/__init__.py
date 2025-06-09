from pathlib import Path
from .context_manager import ContextManager, ContextError, ContextPermissionError
from .repo_handler import RepoHandler
from .syntax_checker import check_syntax
from .logger import CSVLogger

# Compatible with both containers and local runs.
# Must be overwritten before every use
context = ContextManager(Path.cwd())