import csv
import io
import logging
import os
import sys


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
    }
    RESET_CODE = '\033[0m'

    def format(self, record):
        level_name = record.levelname
        color = ColoredFormatter.COLOR_CODES.get(
            level_name, ColoredFormatter.RESET_CODE)
        message = super().format(record)
        return f"{color}{message}{self.RESET_CODE}"


class CSVFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow([record.levelname, record.msg])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


class AgentLogger(logging.Logger):
    def __init__(
            self, name, level=logging.INFO,
            handlers: list[logging.Handler] = None
    ):
        logging.Logger.__init__(self, name, level)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid adding handlers multiple times
        if not self.logger.hasHandlers():
            for handler in handlers:
                self.logger.addHandler(handler)

    def get(self) -> logging.Logger:
        return self.logger


 # Console handler with colors
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = ColoredFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(console_formatter)

# File handler with CSV formatting
file_path = "text.csv"
is_new_file = not os.path.exists(file_path)
file_handler = logging.FileHandler(file_path, mode='a', encoding='utf-8')

fieldnames = ['timestamp', 'logger', 'level', 'message', 'filename', 'lineno', 'funcName']
csv_formatter = CSVFormatter()
file_handler.setFormatter(csv_formatter)

# Optional: write header row if file was just created
if is_new_file:
    with open(file_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


# Instantiate logger configuration
logger = AgentLogger(
    name=__name__,
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

