#!/bin/bash

# Touch the log file to ensure it exists
touch "$STATS_LOG"
touch "$RESULTS_LOG"

# Run the Python script and redirect stdout and stderr to the log file
python benchmark.py
python benchmark.py
