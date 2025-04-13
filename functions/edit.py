import os
from llm import context


edit_tool = {
    "type": "function",
    "function": {
        "name": "edit",
        "description": "Edits an already opened file. An interval is specified,"
                       "between which all code is changed to the given content."
                       "Useful while debugging, or removing unwanted code. For"
                       "creating new features please use the insert tool."
                       "Break down large edit into logically structured small edits instead.",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "number",
                    "description": "Marks the beginning of the interval"
                                   "where the code snippet should be replaced."
                                   "The number for the first line in a file is 1"
                },
                "end": {
                    "type": "number",
                    "description": "The last line that will still be replaced."
                },
                "code": {
                    "type": "string",
                    "description": "The python code to be inserted between the lines."
                                   "Line indentations should be"
                }
            },
            "required": ["start", "end", "code"],
            "additionalProperties": False
        }
    }
}


def edit(start: int, end: int, code: str) -> str:
    file_path = context.get_abs()
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        total_lines = len(lines)

        if start < 1 or end > total_lines or start > end:
            return (
                f"Error: Invalid range. The file has {total_lines} lines, "
                f"but received start_line={start} and end_line={end}."
            )
        # Prepare new content as a list of lines with newline characters
        new_lines = [line if line.endswith('\n') else line + '\n' 
                     for line in code.splitlines()]
        old_lines = [line if line.endswith('\n') else line + '\n' 
                     for line in lines[start - 1:end]]

        # Replace the target lines
        updated_lines = (
            lines[:start - 1] +
            new_lines +
            lines[end:]
        )
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)
        total = len(updated_lines)
        after = total - end

        header = [f"[File: {context.get()} ({total} lines in total)]"]
        old_lines = [f"{i + start}: {line.rstrip()}"
                   for i, line in enumerate(old_lines)]
        separator = [f"(Changed to)"]
        new_lines = [f"{i + start}: {line.rstrip()}"
                     for i, line in enumerate(new_lines)]
        footer = [f"({after} lines after)" if after > 0 else "(end)"]
        return "\n".join(header + old_lines + separator + new_lines + footer)

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {e}"