sudo apt-get install uwsgi-plugin-python3

gunicorn -c gun.py manage:app
