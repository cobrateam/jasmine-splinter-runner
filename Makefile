all: test

dependencies: nose coverage

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

test: dependencies clean
	@nosetests --verbosity=2 --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=jasmine_runner

clean:
	@echo -n 'Cleaning... '
	@find . -name "*.pyc" -delete
	@echo 'done.'
