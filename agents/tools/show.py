from smolagents import tool
from utils import context


#  Extracts a portion of a Python file, numbers each line,
#  and includes information about how many lines exist before and after the snippet

@tool
def show_code(start: int, end: int) -> str:
    """
    Extracts and formats a snippet of code from the last opened file,
    numbering each line. Returns the code of the last opened file from
    the start to end.
    Args:
        start (int): The first line to show
        end (int): The last line to show
    Returns:
        str: A formatted string where each line of code is numbered.
        Before and after the code there is additional context information.
    """
    file_path = context.get_abs()
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        total_lines = len(lines)

        # Validate line interval
        start = max(start, 1)
        start = min(start, total_lines - 1)
        end = min(end, total_lines - 1)
        end = max(end, 1)

        # Format resonse
        total = len(lines)
        before = start - 1
        after = total - end

        header = (f"[File: {context.get()} ({total} lines in total)]\n"
                  f"({before} lines before)") if before > 0 else "(start)"
        snippet = [f"{i + start}: {line.rstrip()}"
                   for i, line in enumerate(lines[start - 1:end])]
        footer = f"({after} lines after)" if after > 0 else "(end)"
        return "\n".join([header] + snippet + [footer]).strip()

    except FileNotFoundError:
        return (f"Error: File '{file_path}' not found in current directory."
                f"Use the list function to list all the content")
    except Exception as e:
        return f"Error: {e}"