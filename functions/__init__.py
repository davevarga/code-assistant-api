import package_import
from functions import create, edit, find, insert, open, run, search, show

# Provide the function calls to EventHandler
tools = [
    create.create_file_or_directory,
    edit.edit_file,
    find.find_file,
    insert.insert_code,
    open.open_file_or_directory,
    run.run_python,
    search.search_dir_for_matches,
    show.show_code,
    package_import.authorize_imports,
]

