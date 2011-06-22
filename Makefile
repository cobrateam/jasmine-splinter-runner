all: test

dependencies: specloud coverage

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install specloud

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

test: dependencies clean
	@specloud --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=jasmine_runner

clean:
	@echo -n 'Cleaning... '
	@find . -name "*.pyc" -delete
	@echo 'done.'
