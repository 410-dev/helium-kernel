#!/bin/bash

# Create directories
mkdir -p data/cache
mkdir -p data/files
mkdir -p data/commands

# Copy defaults/config.json to data/config.json
python3 kernel/bootprep.py --target ./ --registry defaults/registry-installer
