import os
from llm import context


# Open the file in the context of the llm.
# Save the file_name for following commands
open_tool = {
    "type": "function",
    "function": {
        "name": "open",
        "description": "This function let's you navigate in the working directory."
                       "or open a file for editing. It cannot leave the root directory."
                       "To go back use the command with the argument: ../",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Relative path from the current dir to the the target"
                                   "file or directory."
                }
            },
            "required": ["file_name"],
            "additionalProperties": False
        }
    }
}


def open(name) -> str:
    try:
        context.set(name)
        new_context = context.get()
        # We know that it existss
        return f"['{new_context}' opened successfully]"
    except FileNotFoundError:
        return (f"File or directory does not exist in the {context.get()} directory. "
              f"Use the list function to list all the content "
              f"in the current working directory")
    except PermissionError:
        return (f"{name} is outside of the root directory "
                f"Please stay inside the root directory.")