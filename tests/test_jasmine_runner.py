import os
import sys
import mocker

from jasmine_runner.commands import run_specs
from StringIO import StringIO

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
FIXTURES_ROOT = os.path.join(TESTS_ROOT, 'fixtures')

path_to_file = lambda filename: 'file://%s' % (os.path.join(FIXTURES_ROOT, filename))

class TestJasmineRunner(mocker.MockerTestCase):

    def setUp(self):
        self._buf = StringIO()
        self._stdout = sys.stdout
        sys.stdout = self._buf

    def tearDown(self):
        sys.stdout = self._stdout
        self.mocker.reset()

    def assert_printed(self, value):
        self._buf.seek(0)
        assert value in self._buf.read()

    def test_should_print_the_resume_of_the_spec_running_for_passed_specs(self):
        "should print the resume of the spec running for passed specs"
        run_specs(path_to_file('passed-specs.html'))
        self.assert_printed('4 specs, 0 failures in 0.031s')

    def test_should_print_the_resume_of_the_spec_running_for_failed_specs(self):
        "should print the resume of the spec running for failed specs"
        run_specs(path_to_file('failed-specs.html'))
        self.assert_printed('4 specs, 1 failure in 0.028s')

    def test_green_resume(self):
        "should print a green resume for passed specs"
        colored = self.mocker.replace('termcolor.colored')
        colored(mocker.ANY, 'green')
        self.mocker.result('bla')
        self.mocker.replay()

        run_specs(path_to_file('passed-specs.html'))
        self.assert_printed('bla')

        self.mocker.verify()

    def test_red_resume(self):
        "should print a red resume for failed specs"
        colored = self.mocker.replace('termcolor.colored')
        colored(mocker.ANY, 'red')
        self.mocker.result('bla')
        self.mocker.replay()

        run_specs(path_to_file('failed-specs.html'))
        self.assert_printed('bla')

        self.mocker.verify()
