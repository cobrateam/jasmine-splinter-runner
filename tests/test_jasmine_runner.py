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

    def _mock_colored_output(self, color):
        colored = self.mocker.replace('termcolor.colored')
        colored(mocker.ANY, color)
        self.mocker.result('bla')
        self.mocker.replay()

    def _mock_exit(self, w=mocker.ANY):
        exit = self.mocker.replace('sys.exit')
        exit(w)

    def test_should_print_the_resume_of_the_spec_running_for_passed_specs(self):
        "should print the resume of the spec running for passed specs"
        run_specs(path_to_file('passed-specs.html'))
        self.assert_printed('4 specs, 0 failures in 0.031s')

    def test_should_print_the_resume_of_the_spec_running_for_failed_specs(self):
        "should print the resume of the spec running for failed specs"
        run_specs(path_to_file('failed-specs.html'))
        self.assert_printed('4 specs, 2 failures in 0.028s')

    def test_green_resume(self):
        "should print a green resume for passed specs"
        self._mock_colored_output('green')

        run_specs(path_to_file('passed-specs.html'))
        self.assert_printed('bla')

        self.mocker.verify()

    def test_red_resume(self):
        "should print a red resume for failed specs"
        self._mock_colored_output('red')

        run_specs(path_to_file('failed-specs.html'))
        self.assert_printed('bla')

        self.mocker.verify()

    def test_splinter_driver(self):
        "should be able to customize the splinter driver to use"
        from splinter.browser import Browser
        chrome_mock = Browser('webdriver.firefox')
        firefox_mock = Browser('webdriver.firefox')

        Browser = self.mocker.replace('splinter.browser.Browser')
        Browser('webdriver.chrome')
        self.mocker.result(chrome_mock)

        Browser('webdriver.firefox')
        self.mocker.result(firefox_mock)
        self.mocker.replay()

        run_specs(path_to_file('failed-specs.html'), browser_driver='webdriver.chrome')
        run_specs(path_to_file('passed-specs.html'), browser_driver='webdriver.firefox')

        self.mocker.verify()

    def test_firefox_default_driver(self):
        "when no driver is specified, Firefox should be used"
        from splinter.browser import Browser
        browser = Browser('webdriver.firefox')

        Browser = self.mocker.replace('splinter.browser.Browser')
        Browser('webdriver.firefox')
        self.mocker.result(browser)
        self.mocker.replay()

        run_specs(path_to_file('passed-specs.html'))

        self.mocker.verify()

    def test_exit_status(self):
        "should return the proper exit status (very useful for continuous integration jobs)"
        assert 0 == run_specs(path_to_file('passed-specs.html'))
        assert 2 == run_specs(path_to_file('failed-specs.html'))

    def test_main_with_default_options(self):
        "should look for a SpecRunner.html file in the current directory by default"
        getcwd = self.mocker.replace('os.getcwd')
        getcwd()
        self.mocker.result(FIXTURES_ROOT)
        self._mock_exit()
        self.mocker.replay()

        from jasmine_runner.commands import main
        main(args=['jasmine-splinter'])

        self.mocker.verify()

    def test_specify_filepath(self):
        "should be able to specify the filepath"
        self._mock_exit(w=0)
        self.mocker.replay()

        from jasmine_runner.commands import main
        main(args=['jasmine-splinter', '--filepath=%s' % os.path.join(FIXTURES_ROOT, 'passed-specs.html')])

        self.mocker.verify()

    def test_specify_url(self):
        "should be able to specify the url of the runner"
        self._mock_exit(w=0)
        self.mocker.replay()

        from jasmine_runner.commands import main
        main(args=['jasmine-splinter', '--url=%s' % path_to_file('passed-specs.html')])

        self.mocker.verify()

    def test_choose_the_splinter_driver(self):
        "should be able to choose the splinter driver from command line"
        from splinter.browser import Browser
        browser = Browser('webdriver.firefox')

        self._mock_exit(w=0)
        Browser = self.mocker.replace('splinter.browser.Browser')
        Browser('webdriver.chrome')
        self.mocker.result(browser)
        self.mocker.replay()

        from jasmine_runner.commands import main
        main(args=['jasmine-splinter', '--browser-driver=webdriver.chrome', '--url=%s' % path_to_file('passed-specs.html')])

        self.mocker.verify()

    def test_the_first_argument_can_be_a_file_path(self):
        "should be able to specify a url or file path"
        self._mock_exit(w=0)
        self.mocker.replay()

        from jasmine_runner.commands import main
        main(args=['jasmine-splinter', os.path.join(FIXTURES_ROOT, 'passed-specs.html')])

        self.mocker.verify()

    def test_the_first_argument_can_be_a_url(self):
        "should be able to specify a url or file path"
        self._mock_exit(w=0)
        self.mocker.replay()

        from jasmine_runner.commands import main
        main(args=['jasmine-splinter', path_to_file('passed-specs.html')])

        self.mocker.verify()


