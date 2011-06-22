import os
import sys
import unittest

from jasmine_runner.commands import run_specs
from StringIO import StringIO

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
FIXTURES_ROOT = os.path.join(TESTS_ROOT, 'fixtures')

path_to_file = lambda filename: 'file://%s' % (os.path.join(FIXTURES_ROOT, filename))

class TestJasmineRunner(unittest.TestCase):

    def setUp(self):
        self._buf = StringIO()
        self._stdout = sys.stdout
        sys.stdout = self._buf

    def tearDown(self):
        sys.stdout = self._stdout

    def test_shold_print_the_resume_of_the_spec_running_for_passed_specs(self):
        run_specs(path_to_file('passed-specs.html'))

        self._buf.seek(0)
        content = self._buf.read()
        assert '4 specs, 0 failures in 0.031s' in content

    def test_shold_print_the_resume_of_the_spec_running_for_failed_specs(self):
        run_specs(path_to_file('failed-specs.html'))

        self._buf.seek(0)
        content = self._buf.read()
        assert '4 specs, 1 failure in 0.028s' in content
