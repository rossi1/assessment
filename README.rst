assessement_test
================

assesement test

Basic Commands
--------------
Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy assessement_test

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Installion
----------

1. Clone the repository and create a Virtual Environment.
    - Run `virtualenv <virtualenvname>` to create the virtual environment or `mkvirtualenv <virtualenvname>` if using virtualenv wrapper to create the virtual environment.
2. Install all the necessary requirements by running `pip install -r requirements.txt` within the virtual environment.
3. Configure your database configurations in a *base.py* and save in the settings folder
4. Create a *.env* to hold all your environment variables, like your secret key, save in the same level as your README.md file (sample shown below)
##### Sample .env format


DJANGO_READ_DOT_ENV_FILE=True
DATABASE_URL=postgres://project_slug
DJANGO_ADMIN_URL=‘admin/’
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=SECRET_KEY
DJANGO_SECURE_BROWSER_XSS_FILTER=True
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=True
DJANGO_SECURE_FRAME_DENY=True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SESSION_COOKIE_HTTPONLY=True
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_DEFAULT_FROM_EMAIL=“your_project_name <noreply@your_domain_name>”
DJANGO_SERVER_EMAIL=“your_project_name <noreply@your_domain_name>”
DJANGO_EMAIL_SUBJECT_PREFIX=“[your_project_name] “
DJANGO_ALLOWED_HOSTS=[‘your_domain_name’]

6. Run `cd` to navigate into the project directory
7. Run `python manage.py collectstatic` to copy all your static files into the staticfiles directory
8. Run `python manage.py makemigrations` and `python manage.py migrate` to create the necessary tables and everything required to run the application.
9. Run `python manage.py runserver` to run the app.
10. Run `coverage run manage.py test` to know how much the app is covered by automated testing.
11. Run `coverage report` to view the report of the coverage on your terminal.
12. Run `coverage html` to produce the html of coverage result.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^
Run these commands to deploy the project to Heroku:

heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

heroku addons:create heroku-postgresql:hobby-dev
# On Windows use double quotes for the time zone, e.g.
# heroku pg:backups schedule --at "02:00 America/Los_Angeles" DATABASE_URL
heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
heroku pg:promote DATABASE_URL

heroku addons:create heroku-redis:hobby-dev

heroku addons:create mailgun:starter

heroku config:set PYTHONHASHSEED=random

heroku config:set WEB_CONCURRENCY=4

heroku config:set DJANGO_DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"

# Generating a 32 character-long random string without any of the visually similar characters "IOl01":
heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"

# Set this to your Heroku app url, e.g. 'bionic-beaver-28392.herokuapp.com'
heroku config:set DJANGO_ALLOWED_HOSTS=

git push heroku master

heroku run python manage.py createsuperuser

heroku run python manage.py check --deploy

heroku open


Docker
^^^^^^

Before you begin, check out the production.yml file in the root of this project. Keep note of how it provides configuration for the following services:

django: your application running behind Gunicorn;
postgres: PostgreSQL database with the application’s relational data;
redis: Redis instance for caching;
traefik: Traefik reverse proxy with HTTPS on by default.

You will need to build the stack first. To do that, run:

docker-compose -f production.yml build

Once this is ready, you can run it with:

docker-compose -f production.yml up

To run the stack and detach the containers, run:

docker-compose -f production.yml up -d

To run a migration, open up a second terminal and run:

docker-compose -f production.yml run --rm django python manage.py migrate

To check the logs out, run:

docker-compose -f production.yml logs

If you want to scale your application, run:

docker-compose -f production.yml scale django=4

don’t try to scale postgres, or traefik.

To see how your containers are doing run:

docker-compose -f production.yml ps
