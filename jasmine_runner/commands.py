#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import os
import re
import sys
import warnings

from splinter.browser import Browser
from extractors.jasmine import Extractor as JExtractor
from extractors.qunit import Extractor as QExtractor
from reporters.stdout import print_result

class TestSuiteNotDetectedError(Exception):
    pass

def run_specs(path_or_paths, browser_driver='firefox'):
    print
    print 'Using %s as webdriver.' % browser_driver

    paths = path_or_paths
    if not isinstance(paths, (list, tuple)):
        paths = [path_or_paths]

    failures = 0
    browser = Browser(browser_driver)

    for path in paths:
        print
        print 'Running %s ...' % path
        browser.visit(path)

        try:
            Extractor = filter(lambda e: e.is_it_me(browser), [JExtractor, QExtractor])[0]
        except IndexError:
            raise TestSuiteNotDetectedError('test suite not detected.')

        extractor = Extractor(browser)
        extractor.wait_till_finished_and_then(print_result)

        failures += extractor.failures_number

    browser.quit()

    return failures


def has_scheme(uri):
    return bool(re.match(r'^[^:]+://', uri))

def fix_path(uri):
    if has_scheme(uri):
        return uri
    else:
        return 'file://%s' % os.path.abspath(uri)

def main(args=sys.argv):
    ''' Runs Jasmine specs via console. '''
    current_directory = os.getcwd()
    default_runner_path = 'file://%s' % os.path.join(current_directory, 'SpecRunner.html')

    parser = argparse.ArgumentParser(description=u'Run your jasmine specs from command line using splinter')
    parser.add_argument('uri', metavar='URI', nargs='*', help='file path or url to runner file', default=None)
    parser.add_argument('-b', '--browser-driver', metavar='browser_driver', help='splinter driver to use', default='firefox')
    #deprecated args
    parser.add_argument('-f', '--filepath', metavar='FILEPATH', help='path to runner file (deprecated)', default=None)
    parser.add_argument('-u', '--url', metavar='URL', help='url to runner (deprecated)', default=None)

    args = args[1:]
    args = parser.parse_args(args)

    if args.uri:
        runner_path = [fix_path(uri) for uri in args.uri]

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

if __name__ == '__main__':
    main()
