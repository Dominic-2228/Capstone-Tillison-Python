rm db.sqlite3
rm -rf ./api/migrations
python3 manage.py migrate
python3 manage.py makemigrations api
python3 manage.py migrate api
python3 manage.py loaddata user
python3 manage.py loaddata Packages
python3 manage.py loaddata Reviews
python3 manage.py loaddata Services
python3 manage.py loaddata Booking_times
python3 manage.py loaddata Package_services