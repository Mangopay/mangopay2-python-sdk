# These targets are not files
.PHONY: coverage test

test:
	python test_suite.py

coverage:
	coverage run --source=mangopaysdk test_suite.py	