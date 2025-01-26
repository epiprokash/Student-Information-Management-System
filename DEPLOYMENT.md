# Deploying django application on nginx to an Ubuntu server using gunicorn

Before starting, we need an access to an Ubuntu server. We can create an Ubuntu server on AWS, Azure or GCP.

1. First, login to the Ubuntu server and install required softwares

```bash
ssh user@<server ip>
or
ssh -i /path/to/key.pem user@<server ip>

sudo apt install python3 python3-venv python3-pip
```

2. Copy project source to server (execute this on your local machine)

```bash
scp -r django_project user@hostname:/home/user
or
scp -i /path/to/key.pem -r django_project user@hostname:/home/user
```

> _NOTE:_ on Windows machines, `ssh` and `scp` operations may need to be done with
> third party clients such as [PuTTy](https://www.putty.org/)

Edit `settings.py` and remove `insecure` from `SECRET_KEY`. Also, set DEBUG=False
```bash
DEBUG=False
```

> _NOTE:_ no matter what keep your `SECRET_KEY` secret if you want to keep your app secure.
> You may want to use `SECRET_KEY` different from development on your production app.

Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Give credentials to `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dbname',
    }
}
```

Migrate database schema
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Ready staticfiles. First edit `settings.py`
```python
STATIC_URL = 'static/'
STATIC_ROOT = 'staticfiles/'

STATICFILES_DIRS = [
    BASE_DIR / 'students/static',
    '/home/user/staticfiles',
]
```

Then ready staticfiles directories
```bash
mkdir django_project/staticfiles
ln -s django_project/staticfiles /home/user
python manage.py collectstatic
```


6. Install gunicorn and create configuration file
```bash
pip install gunicorn
sudo apt install gunicorn
touch gunicorn_conf.py
```

Make config
```python
command = '/home/user/venv/bin/gunicorn'
pythonpath = '/home/user/django_project'
bind = '127.0.0.1:8000'
workers = 3
```

Run project using gunicorn in foreground to check if it works correctly. Then press `CTRL+Z` and enter `bg` to push it the background.
```bash
gunicorn -c gunicorn_conf.py django_project.wsgi
```

7. Configure and run nginx
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/example.com
```

nginx server block:
```
server {
    listen 80;
    server_name www.example.com;

    location /static {
        alias /home/user/staticfiles;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Reload nginx
```bash
sudo nginx -s reload
```

The site should now be accessible at http://example.com

8. Secure nginx with SSL

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```
Provide necessary details. The path to SSL files and https redirection should be automatically added to the nginx config by cerbot,
Reload nginx to apply the change in effect.

```bash
sudo nginx -s reload
```

The site now should be accessible at https://example.com

9. Finally fix csrf validation issue by adding proper hostname to `ALLOWED_HOST` and `CSRF_TRUSTED_ORIGINS`

```python
ALLOWED_HOSTS = ['example.com', '127.0.0.1', '<server ip>']

CSRF_TRUSTED_ORIGINS = [
    'http://.*',
    'https://example.com',
    'https://<server ip>',
    'http://127.0.0.1',
]
```

Now users will be able to post form without any errors.


10. Finally, if everything works correctly it's time to setup a daemon which will run the application every time the server machine boots up.

```bash
sudo nano /etc/systemd/system/myproject.service
```

Copy paste the following:

```
[Unit]
Description=Django Web Application

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/django_project
ExecStart=/home/user/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/user/django_project.sock django_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Save and exit then try to run
```bash
sudo systemctl start myproject
```

If no errors shown then we can finally enable the service
```bash
sudo systemctl enable myproject
```
