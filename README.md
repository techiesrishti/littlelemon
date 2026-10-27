# Little Lemon - Booking Back-End (Django + MySQL)

Project directory: `littlelemon`  |  App: `restaurant`

## 1. Prerequisites
- Python 3.9+ and `pipenv`
- MySQL Server running locally
- (macOS) `brew install mysql pkg-config`  |  (Ubuntu) `sudo apt install libmysqlclient-dev pkg-config build-essential python3-dev`
  (needed to build the `mysqlclient` package)

## 2. Create the MySQL database
```sql
CREATE DATABASE littlelemon;
```

## 3. Set your MySQL credentials
Open `littlelemon/settings.py` -> `DATABASES` and change USER / PASSWORD
(or set env vars `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, `DB_PORT`).

## 4. Install and run
```bash
cd littlelemon
pipenv shell
pipenv install
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata menu        # optional: sample menu items
python manage.py runserver
```

## 5. Pages / endpoints
| URL | What it does |
|---|---|
| http://127.0.0.1:8000/book/ | Booking form (name, date picker, time slot) + bookings for the chosen date |
| http://127.0.0.1:8000/reservations/ | All bookings shown as JSON |
| http://127.0.0.1:8000/bookings | API: all bookings (JSON); POST creates a booking |
| http://127.0.0.1:8000/bookings?date=2022-12-13 | API: bookings for one date |
| http://127.0.0.1:8000/menu/ | Menu |
| http://127.0.0.1:8000/admin/ | Admin (`python manage.py createsuperuser`) |
