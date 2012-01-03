.PHONY: clean test docs dist check_release

all: clean test

test:
	python setup.py test 

tox-test:
	PYTHONDONTWRITEBYTECODE= tox

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	python setup.py clean

docs:
	$(MAKE) -C docs html

dist:
	python setup.py sdist

install:
	python setup.py install

check_release:
	python setup.py --long-description | rst2html.py