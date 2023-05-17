#!/bin/bash

# Define color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if pip3 and python3 are installed
if [[ $(command -v pip3) == "" ]]; then
    echo -e "${RED}Error: pip3 is not installed. Please install it and try again.${NC}"
    exit 1
fi

if [[ $(command -v python3) == "" ]]; then
    echo -e "${RED}Error: python3 is not installed. Please install it and try again.${NC}"
    exit 1
fi


echo -e "${NC}Starting kernel...${NC}"
python3 core.py "$@" --bootfile 

# If argument contains --clear-cache then remove all directories named __pycache__
if [[ $1 == "--clear-cache" ]]; then
    echo -e "${YELLOW}Clearing cache...${NC}"
    find . -name "__pycache__" -type d -exec rm -rf {} \; 2>/dev/null
    rm -rf data/cache 2>/dev/null
    echo -e "${GREEN}Cache cleared.${NC}"
fi


echo -e "${NC}Kernel stopped.${NC}"
exit 0
