#!/bin/bash
rm -rf registry

if [[ "$*" == *"--data"* ]]; then
    rm -rf data
fi
