from .context_manager import ContextManager
from .repo_handler import RepoHandler
from .syntax_checker import check_syntax
from .logger import CSVLogger

# Instantiation takes place now, so that certain
# function calling tools can manipulate the context.
context = ContextManager('D:/Projects/code-assistant-api')