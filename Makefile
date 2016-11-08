install:
	pip install -r requirements/base.txt

test:
	nosetests -s tests --with-coverage --cover-erase --cover-package=tests

release:
	python setup.py sdist register upload -s
