all: test

dependencies: coverage mocker nose argparse termcolor splinter

termcolor:
	@python -c 'import termcolor' 2>/dev/null || pip install termcolor==1.1.0

argparse:
	@python -c 'import argparse' 2>/dev/null || pip install argparse==.1.2.1

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage==.3.5b1

mocker:
	@python -c 'import mocker' 2>/dev/null || pip install mocker==1.1

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose==1.0.0

splinter:
	@python -c 'import splinter' 2>/dev/null || pip install splinter==0.2

test: dependencies clean
	@nosetests --verbosity=2 --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=jasmine_runner

clean:
	@echo -n 'Cleaning... '
	@find . -name "*.pyc" -delete
	@echo 'done.'
