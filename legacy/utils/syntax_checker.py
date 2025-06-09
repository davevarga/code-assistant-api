import ast

def check_syntax(code: str):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return [f"Invalid syntax {e}"]