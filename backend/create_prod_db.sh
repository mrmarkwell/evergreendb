./archive_db.sh
mkdir -p app/static/photos app/static/medical app/static/interactions
python db_create.py
python db_seed.py
