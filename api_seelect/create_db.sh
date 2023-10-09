#!/bin/bash

# Deleting db
rm db.sqlite3

# Deleting Users Migrations
cd ./users
rm -r migrations
cd ../
# Deleting Auth Migrations
cd ./authentication
rm -r migrations
cd ../
# Deleting Contact Migrations
cd ./contact
rm -r migrations
cd ../
# Deleting Events Migrations
cd ./events
rm -r migrations
cd ../
# Deleting Kits Migrations
cd ./kits
rm -r migrations
cd ../

python manage.py makemigrations users
python manage.py makemigrations authentication
python manage.py makemigrations contact
python manage.py makemigrations events
python manage.py makemigrations kits
python manage.py migrate

#python3 manage.py loaddata db/db_user.json
#python3 manage.py loaddata db/db_forms.json
#python3 manage.py loaddata db/db_analysis.json