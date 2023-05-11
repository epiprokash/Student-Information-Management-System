# Deploying django application with PostgreSQL on nginx to an Ubuntu server using gunicorn

Most of the setup will be similar to the default setup. With some extra steps:

 - psycopg2 (psql driver for django) needed to connect to a psql server from your Django app.

```bash
source venv/bin/activate
pip install psycopg2
pip freeze > requirements.txt
```

> _NOTE:_ Sometimes pip may alert you for psycopg2 installation failing. In that case, try to install
> psycopg2-binary instead.
> 
> ```bash
> pip install psycopg2-binary
> ```

 - Instead of setting up sqlite superuser, setup PostgreSQL server

```bash
sudo apt install postgresql
sudo pg_ctlcluster <version> main start
psql -U postgres -d postgres
```

Create user and database for the application to use
```sql
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE database;
GRANT ALL ON DATABASE database TO admin;
```

Sign in using the user to check
```bash
psql -U admin -d database -W
```

 - Give credentials to `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Migrate database schema
```bash
python manage.py makemigrations
python manage.py migrate
```

The rest of the procedure should be similar to the default.
