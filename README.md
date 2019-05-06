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
cd backend
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
cd backend
source virtualize.sh
./create_prod_db.sh // Or create_test_db.sh to populate some test data
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

# Frontend Quick Start Guide

To get started using the frontend follow these steps:

Install node.js:  
Ubuntu: https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions  
Windows: https://nodejs.org/en/download/

Install dependencies and run app:  
```
cd fss 
npm install

// To test in browser and attach vscode debugger
ng serve

// To run in electron locally with source mapping
npm run slowstart

// To run in electron locally without source mapping (faster)
npm run faststart

```

Package app as executable:
```
npm run packagelocal # for current OS
npm run packageall # for all OSs
```

# Backend EC2 Deploy guide

Taken roughly from this tutorial: https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/

```
ssh -i /path/to/your/keyfile ec2-user@your_public_dnsname_here
```
if you need any info for the command above... you are going to need more help than this guide

Change to the apps user, and go to the evergreen dir that was already created:
```
[ec2-user@ip-172-31-14-180 ~]$ sudo su apps
[apps@ip-172-31-14-180 ~]$ cd ~/evergreendb
```
Clone git repo or if already cloned just do a git pull to grab the latest version
```
[apps@ip-172-31-14-180 ~]$ git pull
```
Setup virtual env if its not already setup following directions in the link above then source the virtualenv and install any new python packages:
```
[apps@ip-172-31-14-180 evergreendb]$ cd backend/
[apps@ip-172-31-14-180 backend]$ source virtualize.sh
[apps@ip-172-31-14-180 evergreendb]$ pip install -r requirements.txt
```
At this point you can setup nginx as the web server following directions in the link but it should be done already.
Finally kill any gunicorn processes and restart them:
```
[apps@ip-172-31-14-180 evergreendb]$ pkill gunicorn
[apps@ip-172-31-14-180 evergreendb]$ gunicorn app:app -b localhost:8000 --error-logfile /home/apps/logs/error.log &
```

# Developer Tips

## Start the backend locally

```bash
cd backend
source virtualize.sh
./create_prod_db.sh // Or create_test_db.sh to populate some test data
python run.py
```

## Update NPM

```bash
cd fss
npm i -g npm
```

## Install all packages in package.json

```bash
cd fss
npm install
```

## Update the version of the product

```bash
# Edit VERSION file with correct version
./update_version.sh
```

### Check the version of the front end

Navigate to the Settings page of the app to see it.

### Check the version of the back end

Navigate to the /version endpoint to see it.
