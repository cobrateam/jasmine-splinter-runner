from setuptools import setup, find_packages
from jasmine_runner import __version__

README = open('README.rst').read()

setup(name='jasmine-splinter-runner',
      version=__version__,
      description='jasmine runne based on splinter',
      long_description=README,
      author='CobraTeam',
      author_email='francisco@franciscosouza.net',
      packages=find_packages(),
      include_package_data=True,
      test_suite='nose.collector',
      install_requires=['splinter', 'termcolor'],
      entry_points = {
          'console_scripts' : [
              'jasmine-splinter = jasmine_runner.commands:main',
          ]
      },
     )

