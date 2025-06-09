# This file contains demo code for testing purposes.
# test_module.py

# This is a sample module for testing indentation normalization.
# It includes various Python elements.

import math

def logger(func):
    """A simple decorator that logs function calls."""
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class Calculator:
    """A basic calculator class."""

    def __init__(self, initial=0):
        self.value = initial

    def add(self, x):
        """Adds x to the current value."""
        self.value += x
        return self.value

    def multiply(self, x):
        """Multiplies the current value by x."""
        self.value *= x
        return self.value

    def reset(self):
        """Resets the calculator."""
        self.value = 0

    def __str__(self):
        return f"Calculator(value={self.value})"


@logger
def compute_area(radius):
    """Computes the area of a circle given the radius."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    area = math.pi * radius ** 2
    return area


def main():
    # Main execution logic
    calc = Calculator()
    print("Initial:", calc)

    calc.add(10)
    calc.multiply(2)
    print("Updated:", calc)

    area = compute_area(5)
    print("Area:", area)

    try:
        compute_area(-1)
    except ValueError as e:
        print("Caught error:", e)

if __name__ == "__main__":
    main()