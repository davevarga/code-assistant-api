from .create import create_file_or_directory
from .edit import edit_file
from .find import find_file
from .insert import insert_code
from .open import open_file_or_directory
from .run import run_python
from .search import search_dir_for_matches
from .show import show_code
from .package_import import authorize_imports


# Provide the function calls to EventHandler
toolset = [
    create_file_or_directory,
    edit_file,
    find_file,
    insert_code,
    open_file_or_directory,
    run_python,
    search_dir_for_matches,
    show_code,
    authorize_imports,
]

