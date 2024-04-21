#!/bin/bash

outputDir="output"
mkdir -p "$outputDir"

logDir="log"
mkdir -p "$logDir"

configDir="config"
mkdir -p "$configDir"

venvDir=".venv"
if [ ! -d "$venvDir" ]; then
    python -m venv "$venvDir"
    echo "Created python virtual environment at $venvDir."
fi

source "$venvDir/Scripts/activate"
echo "Using python in $venvDir."

echo "Installing dependencies using pip..."
pip install -r requirements.txt
echo "Finished installing."

echo "Running main.py..."
echo "-------------------------------"
python src/main.py
exitCode=$?
echo "-------------------------------"
if [ "$exitCode" -ne 0 ]; then
    echo "Abort!"
fi
echo "Deactivating..."
deactivate
echo "Quit."