import os


def create(file_name):
    try:
        with open(file_name, "w") as file:
            file.write("This is a file")
        return f"{file_name} created successfully"
    except Exception as e:
        return f"{file_name} not created: {str(e)}"


def open_file(file_name):
    if os.path.exists(file_name):
        return f"{file_name} opened successfully"
    else:
        return f"{file_name} does not exist"


