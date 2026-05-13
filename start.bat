@echo off

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt

set FLASK_APP=run.py
flask db upgrade
python seed.py
python run.py
pause
