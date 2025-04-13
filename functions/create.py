import os
from llm import context

# Define a documentation corresponding to chagGPT API.
create_tool = {
    "type": "function",
    "function": {
        "name": "create",
        "description": "Creates either a new directory or file"
                       "with a given extension in the current directory",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the file or directory to be created"
                                   "A file is defined by having an extension."
                }
            },
            "required": ["name"],
            "additionalProperties": False
        }
    }
}

def create(name: str) -> str:
    curr_dir = context.get()
    path = os.path.join(curr_dir, name)

    # Check if is already created
    if os.path.exists(path):
        if os.path.isdir(path):
            return "Directory %s already exists in the current directory" % path
        if os.path.isfile(path):
            return "File %s already exists in the current directory" % path

    # Normalize the path to avoid issues with trailing slashes
    path = os.path.normpath(path)

    # Extract the base name and check for a file extension
    _, extension = os.path.splitext(path)

    if extension:
        with open(path, 'w') as f:
            f.write(f"# File {path}") # Write the path in the file
        return f"File created: {path}"
    else:
        # It's a directory
        os.makedirs(path, exist_ok=True)
        return f"Directory created: {path}"