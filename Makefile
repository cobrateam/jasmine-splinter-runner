all: test

test: clean
	@nosetests --verbosity=2 --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=jasmine_runner

publish:
	python setup.py sdist upload

clean:
	@echo -n 'Cleaning... '
	@find . -name "*.pyc" -delete
	@echo 'done.'

.PHONY: clean publish all test
