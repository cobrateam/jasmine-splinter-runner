#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

from termcolor import colored
from optparse import OptionParser
from splinter.browser import Browser

def run_specs(path):
    print 'Using %s as runner.' % path

    browser = Browser()
    browser.visit(path)

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
    ''' Runs Jasmine specs via console. '''
    current_directory = os.getcwd()
    default_runner_path = os.path.join(current_directory, 'SpecRunner.html')

    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="the runner url", default="")
    parser.add_option("-f", "--file-path", dest="file_path", help="runner file path", default=default_runner_path)

    (options, args) = parser.parse_args()

    if options.url != "":
        runner_path = options.url
    else:
        runner_path = "file://%s" % os.path.abspath(options.file_path)

    sys.exit(run_specs(runner_path))

if __name__ == '__main__':
    main()
