# flask-registration-sqlite
[![PyPI](https://img.shields.io/pypi/pyversions/discord.py.svg)](https://github.com/python)

This is an web app created for a fictitious crypto group enthusiast. The backend support is mostly built with
python with some javascript on the templates. It features the following:
- User registration with user verification through email + token
- User login after verification, with access to different webpages based on role
- Role based permission using decorators
- Database for storage
 

## Prerequisites
- Python 3.4.2+
- Python extensions
- SQLite

## Installation
- Python 3.4.2+ can be downloaded [here](https://www.python.org/)
- SQLite can be downloaded [here](https://www.sqlite.org/)
- You can install Python packages by running pip on your command like:
```
python3 pip install Flask-SQLAlchemy
```
- DBBrowser for SQLite can be downloaded [here](http://sqlitebrowser.org/) (optional)


# QuickStart

### Update Configuration settings

1. Secret key and security salt
2. Database URI
3. Email settings

### Set the configuration settings

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
```

Note: For windows use `set` instead of `export`



### Create the database

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
```

### Run

```sh
$ python manage.py runserver
```