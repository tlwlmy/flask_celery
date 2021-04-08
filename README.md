sudo apt-get install uwsgi-plugin-python3

gunicorn -c gun.py manage:app

sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip

* python3.8安装pycrypto
pip uninstall Crypto
pip uninstall pycrypto
pip install pycryptodome
