from llm import context
import os


find_tool = {
    "type": "function",
    "function": {
        "name": "find",
        "description": "Finds all instances of a filename within the project"
                       "and returns with a list of relative paths from the root",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Search for this file name in the context"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}


def find(filename: str) -> str:
    root_dir = context.get_root_directory()

    matches = []
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if filename in files:
            matches.append(os.path.join(root, filename))

    content = [" - ./" + os.path.relpath(match, root_dir) for match in matches]
    header = [f"[{len(matches)} instances found for '{filename}']"]
    return "\n".join(header + content)