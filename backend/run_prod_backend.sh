mkdir -p ~/backup_logs; mkdir -p ~/logs; mv ~/logs/* ~/backup_logs/;  cd ~/evergreendb/backend/; /home/apps/evergreendb/backend/venv/bin/gunicorn app:app -b localhost:8000 --error-log ~apps/logs/error.log --access-logfile ~apps/logs/evergreen.log &
