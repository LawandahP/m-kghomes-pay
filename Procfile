web: gunicorn core.wsgi --log-file -

release: python3 manage.py makemigrations --noinput
release: python3 manage.py migrate --noinput