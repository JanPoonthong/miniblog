# Miniblog

## Requirements

### Linux & MacOS

Prerequisites:

- [Python][python-download]
- [Django][django-download]

Instructions:

1.  Download Django:

        $ pip install Django==3.2.7

1.  Run:

        $ cd miniblog
        $ ./manage.py migrate --run-syncdb
        $ ./manage.py runserver

        or

        $ cd miniblog
        $ python3 manage.py migrate --run-syncdb
        $ python3 manage.py runserver

After doing `python3 manage.py runserver` check http://127.0.0.1:8000/ or http://localhost:8000/

[django-download]: https://www.djangoproject.com/download/
[python-download]: https://www.python.org/downloads/
