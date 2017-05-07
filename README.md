# evergreendb

[![Join the chat at https://gitter.im/evergreendb/Lobby](https://badges.gitter.im/evergreendb/Lobby.svg)](https://gitter.im/evergreendb/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Database management tool for Evergreen

# TravisCI

[![Build Status](https://travis-ci.org/mrmarkwell/evergreendb.svg?branch=develop)](https://travis-ci.org/mrmarkwell/evergreendb)

# Backend Quick Start Guide

To get started using the backend follow these steps:

For Ubuntu:
'''
pip install virtualenv
sudo apt-get install python-dev
cd flaskplayground
sudo -s
source virtualize.sh # Create the virtualenv
deactivate
exit
sudo source virtualize.sh
python db_create.py
python run.py
'''

For Windows terminal emulator:
'''
pip install virtualenv
cd flaskplayground
source virtualize.sh
python create_db.py
python run.py
'''

