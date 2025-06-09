import os
import pytest
from pathlib import Path
from legacy.agents.utils import CodeFormatter

TEST_FILE = "tests/agents/test_file.py"

TEST_CODE = """        def new_function():
            print("Hello World")
            # This function functions
            return False"""

class TestCodeFormatter:
    @pytest.fixture
    def init_file(self, tmp_path):
        python_code = Path(TEST_FILE).read_text()
        tmp_path = tmp_path / "test_file.py"
        tmp_path.write_text(python_code)
        assert tmp_path.exists(), "File does not exist"
        assert os.access(tmp_path, os.R_OK), "Permission denied for file"
        return tmp_path

    def test_without_change(self, init_file):
        file = init_file
        old_code = file.read_text()
        formatter = CodeFormatter()
        formatter.insert(file, 3, '')
        new_code = file.read_text()
        assert old_code == new_code, "Code should not change"

    def test_insert_after_function(self, init_file):
        file = init_file
        formatter = CodeFormatter()
        assert TEST_CODE.splitlines()[0] == "        def new_function():"
        formatter.insert(file,21, TEST_CODE)
        new_text = file.read_text().splitlines()
        assert new_text[20:26] == [
            "",
            "    def new_function():",
            "        print(\"Hello World\")",
            "        # This function functions",
            "        return False",
            "    def add(self, x):",
        ]

    def test_insert_try_block(self, init_file):
        file = init_file
        formatter = CodeFormatter()
        test_code = TEST_CODE.splitlines()
        test_code = [line.strip() for line in test_code]
        formatter.insert(file, 61, '\n'.join(test_code))
        new_text = file.read_text().splitlines()
        assert new_text[60:67] == [
            "    try:",
            "        def new_function():",
            "        print(\"Hello World\")",
            "        # This function functions",
            "        return False",
            "        compute_area(-1)",
            "    except ValueError as e:",
        ]

