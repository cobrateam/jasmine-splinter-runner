all: test

dependencies: coverage mocker nose argparse termcolor splinter

termcolor:
	@python -c 'import termcolor' 2>/dev/null || pip install termcolor

argparse:
	@python -c 'import argparse' 2>/dev/null || pip install argparse

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

mocker:
	@python -c 'import mocker' 2>/dev/null || pip install mocker

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose

splinter:
	@python -c 'import splinter' 2>/dev/null || pip install splinter

test: dependencies clean
	@nosetests --verbosity=2 --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=jasmine_runner

clean:
	@echo -n 'Cleaning... '
	@find . -name "*.pyc" -delete
	@echo 'done.'
