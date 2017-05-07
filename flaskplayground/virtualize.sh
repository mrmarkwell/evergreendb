# Shell script to make the virtual environment venv
# This script must be sourced, not run in a forked thread!

if [ ! -d "venv" ]; then
    virtualenv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
else
    source venv/Scripts/activate
fi
