#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import os
import sys

from termcolor import colored
from optparse import OptionParser
from splinter.browser import Browser

def run_specs(path, browser_driver='webdriver.firefox'):
    print 'Using %s as runner.' % path

    browser = Browser(browser_driver)
    browser.visit(path)

    runner_div = browser.find_by_css('.runner').first
    passed = 'passed' in runner_div['class']

    if passed:
        color, exit_status = 'green', 0
    else:
        color, exit_status = 'red', 1

    output = browser.find_by_css('.runner span .description').first.text
    browser.quit()

    print colored(output, color)
    return exit_status

def main(args=sys.argv):
    ''' Runs Jasmine specs via console. '''
    current_directory = os.getcwd()
    default_runner_path = os.path.join(current_directory, 'SpecRunner.html')

    parser = argparse.ArgumentParser(description=u'Run your jasmine specs from command line using splinter')
    parser.add_argument('-f', '--filepath', metavar='filepath', help='path to runner file', default=default_runner_path)
    parser.add_argument('-u', '--url', metavar='url', help='url to runner', default=None)
    parser.add_argument('-b', '--browser-driver', metavar='browser_driver', help='splinter driver to use', default='webdriver.firefox')
    args = parser.parse_args(args)

    if args.url:
        runner_path = args.url
    else:
        runner_path = 'file://%s' % args.filepath

    sys.exit(run_specs(runner_path, args.browser_driver))
