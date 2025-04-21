from functions import create, edit, find, insert, list, open, run, search, show

# Provide the function calls to EventHandler
tools = {
    "create": create.create,
    "edit": edit.edit,
    "find": find.find,
    "insert": insert.insert,
    "list": list.lists,
    "open": open.open,
    "run": run.run,
    "search": search.search,
    "show": show.show,
}

# List of available tools for the agent
function_tools = [
    create.create_tool,
    edit.edit_tool,
    find.find_tool,
    insert.insert_tool,
    list.list_tool,
    open.open_tool,
    run.run_tool,
    search.search_tool,
    show.show_tool,
]