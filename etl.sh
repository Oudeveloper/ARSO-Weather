#!/bin/bash

# Define the Python command to use
PYTHON_CMD=python

# Check if python3 command exists
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
fi

# Run the Python scripts
$PYTHON_CMD  xml_downloader.py
$PYTHON_CMD  xml_parser.py
