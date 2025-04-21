from llm import context
import os


list_tool = {
    "type": "function",
    "function": {
        "name": "list",
        "description": "Lists folders and files in the current directory"
                       "Only works if the current context is a folder.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}


def lists() -> str:
    abs_path = context.get_abs()
    rel_path = context.get()
    if not os.path.exists(abs_path):
        return f"{rel_path} does not exist"
    if not os.path.isdir(abs_path):
        return f"{rel_path} is not a directory"
    response = f"The content in the {rel_path} is:\n"
    for content in os.listdir(abs_path):
        response = response + f"-> {content}\n"
    return response