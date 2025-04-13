from llm import context
import os

extensions = ('.py', '.pyi', '.sh', '.bash', '.psi'
              '.toml', '.ini', '.cfg', '.json', '.yaml', '.yml'
              '.md', '.rst', '.txt', '.xml', '.html', '.css', '.js')

search_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Searches through files and directories to find a match for a string"
                       "Starting from the last opened context, it returns all the files and"
                       "lines where match has been found to a given string."
                       "Useful when searching for a function or a class in a project."
                       "It is not recommended to search for variables as similarly named"
                       "variables might have different semantics.",
        "parameters": {
            "type": "object",
            "properties": {
                "template": {
                    "type": "string",
                    "description": "Search operand. The function searches for occurrences "
                                   "of this string in files and subdirectories"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}

def search_file(file_path, query):
    results = []
    try:
        with open(file_path, "r", encoding='utf-8', errors='ignore') as file:
            for i, line in enumerate(file, start=1):
                if query in line:
                    results.append({
                        "path": file_path,
                        "line":i,
                        "snippet":line.strip()
                    })
    except Exception:
        # Skip files that can't be read (e.g., binary files or permission errors)
        pass
    return results



def search(template: str) -> str:
    current_path = context.get_abs()
    root_dir = context.get_root_directory()

    occurrences = []
    if os.path.isfile(current_path):
        occurrences += search_file(current_path, template)

    elif os.path.isdir(current_path):
        for root, dirs, files in os.walk(current_path):
            # Modify dirs in-place to skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    occurrences += search_file(file_path, template)

    content = [
        (f"./{os.path.relpath(occurrence['path'], current_path)}"
         f" at line {occurrence["line"]}\n"
         f"\t '{occurrence['snippet']}'")
        for occurrence in occurrences
    ]
    header = [f"[{len(occurrences)} instances found for '{template}'"
              f" in './{os.path.relpath(current_path, root_dir)}']"]
    return "\n".join(header + content)