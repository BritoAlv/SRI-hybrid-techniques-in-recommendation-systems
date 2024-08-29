#!/bin/bash

# List of Python packages
PACKAGES=(
    "requests"
    "flask"
    "flask_cors"
    "sqlalchemy"
    "numpy"
    "vaderSentiment"
    "faker"
)

# Install each package using pip
for PACKAGE in "${PACKAGES[@]}"; do
  pip install "$PACKAGE"
done
