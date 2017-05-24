# evergreendb

[![Join the chat at https://gitter.im/evergreendb/Lobby](https://badges.gitter.im/evergreendb/Lobby.svg)](https://gitter.im/evergreendb/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Database management tool for Evergreen

# TravisCI

[![Build Status](https://travis-ci.org/mrmarkwell/evergreendb.svg?branch=develop)](https://travis-ci.org/mrmarkwell/evergreendb)

# Backend Quick Start Guide

To get started using the backend follow these steps:

For Ubuntu:
```python
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
```

For Windows terminal emulator:
```
pip install virtualenv
cd flaskplayground
source virtualize.sh
python db_create.py
python run.py
```

# Setting Up Postman

To set up Postman:
- Install Postman and open it
- Select "Import" in the top left-hand corner.
- Import all files in the "postman" folder of the repo.
- Choose the "EvergreenDB" environment from the top right-hand corner of Postman
- Run the backend run.py script on your local system (see Quick Start guide above)
- Choose a Postman request from the EvergreenDB collection on the left side of Postman and click "Send" to execute the request.


