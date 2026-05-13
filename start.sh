#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=run.py
flask db upgrade
python3 seed.py
python3 run.py
