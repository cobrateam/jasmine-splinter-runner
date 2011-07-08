#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import os
import re
import sys
import warnings

from termcolor import colored
from splinter.browser import Browser
from jasmine_runner.string_formatter import format_exit

def run_specs(path, browser_driver='webdriver.firefox'):
    print 'Using %s as runner.' % path

    browser = Browser(browser_driver)
    browser.visit(path)

    while browser.is_text_present("Running..."):
        pass

    runner_div = browser.find_by_css('.runner').first
    passed = 'passed' in runner_div['class']

    output = browser.find_by_css(".runner .description").first.text

    if passed:
        color, exit_status = 'green', 0
        print colored(output, color)
    else:
        failures = int(re.search(r'(\d+)\s*failure', output).group(1))
        color, exit_status = 'red', failures
        print format_exit(browser, output, color)

    browser.quit()

    return exit_status



def has_scheme(uri):
    return bool(re.match(r'^[^:]+://', uri))

def main(args=sys.argv):
    ''' Runs Jasmine specs via console. '''
    current_directory = os.getcwd()
    default_runner_path = 'file://%s' % os.path.join(current_directory, 'SpecRunner.html')

    parser = argparse.ArgumentParser(description=u'Run your jasmine specs from command line using splinter')
    parser.add_argument('uri', metavar='URI', nargs='?', help='file path or url to runner file', default=None)
    parser.add_argument('-b', '--browser-driver', metavar='browser_driver', help='splinter driver to use', default='webdriver.firefox')
    #deprecated args
    parser.add_argument('-f', '--filepath', metavar='FILEPATH', help='path to runner file (deprecated)', default=None)
    parser.add_argument('-u', '--url', metavar='URL', help='url to runner (deprecated)', default=None)

    args = args[1:]
    args = parser.parse_args(args)

    if args.uri:
        if has_scheme(args.uri):
            runner_path = args.uri
        else:
            runner_path = 'file://%s' % args.uri

    # deprecated options
    # when the deprecated options are removed this code can be removed
    elif args.url:
        runner_path = args.url
        warnings.warn(
            '-u and --url options are deprecated, use the url directly instead. Ex: `jasmine-splinter URL`',
            DeprecationWarning
        )
    elif args.filepath:
        runner_path = 'file://%s' % args.filepath
        warnings.warn(
            '-f and --filepath options are deprecated, use the filepath directly instead. Ex: `jasmine-splinter FILEPATH`',
            DeprecationWarning
        )
    #end of depreated options code

    else:
        runner_path = default_runner_path

    sys.exit(run_specs(runner_path, args.browser_driver))
