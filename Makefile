all: virtualenv install

virtualenv:
	virtualenv --python=python3 venv
	source venv/bin/activate; pip install -r requirements.txt

install: /usr/local/bin/notion-cli
	ln -s "$$PWD/__main__.py" /usr/local/bin/notion-cli
