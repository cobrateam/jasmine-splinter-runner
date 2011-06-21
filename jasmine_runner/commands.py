import os
import sys
from splinter.browser import Browser
from termcolor import colored

def run_specs(path):
    browser = Browser()
    browser.visit("file://%s" % path)

    runner_div = browser.find_by_css('.runner').first
    passed = 'passed' in runner_div['class']

    if passed:
        color = 'green'
        exit_status = 0
    else:
        color = 'red'
        exit_status = 1

    output = browser.find_by_css('.runner span .description').first.text
    browser.quit()

    print colored(output, color)
    return exit_status

def main():
    current_directory = os.getcwd()
    runner_path = os.path.join(current_directory, 'SpecRunner.html')
    sys.exit(run_specs(runner_path))

if __name__ == '__main__':
    main()
