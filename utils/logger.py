import os
import csv


fields = [
    'id',
    'inference_time',
    'cloning_time',
    'total_time',
    'input_tokens',
    'output_tokens',
    'attempts',
    'total_steps'
]


class CSVLogger:
    def __init__(self, filepath):
        self.fields = {}
        self.reset()
        self.filepath = filepath
        assert self.fields is not None, "Fields is none"

        # Create the log file.
        if not os.path.exists(filepath):
            with open(self.filepath, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fields.keys())
                writer.writeheader()

    def log(self, field, value):
        self.fields[field] = value if type(value) is str else self.fields[field] + value

    def save(self):
        # Save to log file if every field is defined
        for key, value in self.fields.items():
            assert value != 0, f"Field {key} value not defined"

        with open(self.filepath, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields.keys())
            writer.writerow(self.fields)
            self.reset()

    def reset(self):
        for field in fields:
            self.fields[field] = 0