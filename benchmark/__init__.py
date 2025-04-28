import os
import csv

class CSVLogger:
    def __init__(self, filepath):
        self.fields = None
        self.reset()
        self.filepath = filepath

        # Create the log file.
        if not os.path.exists(filepath):
            with open(self.filepath, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fields.keys())
                writer.writeheader()

    def log(self, field, value):
        assert self.fields[field] is 0, f"Field {field} value overwriting"
        self.fields[field] = value if type(value) is str else self.fields[field] + value

    def save(self):
        # Save to log file if every field is defined
        for key, value in self.fields.items():
            assert value is not 0, f"Field {key} value not defined"

        with open(self.filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields.keys())
            writer.writerow(self.fields)
            self.reset()

    def reset(self):
        self.fields = {
            'id': 0,
            'inference_time': 0,
            'cloning_time': 0,
            'total_time': 0,
            'total_tokens': 0,
            'attempts': 0,
            'total_steps': 0
        }

