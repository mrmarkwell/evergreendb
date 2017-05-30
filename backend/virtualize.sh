# Shell script to make the virtual environment venv
# This script must be sourced, not run in a forked thread!

if [ ! -d "venv" ]; then
    virtualenv venv
    if [ -d "venv/Scripts" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    pip install -r requirements.txt
else
    if [ -d "venv/Scripts" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
fi
