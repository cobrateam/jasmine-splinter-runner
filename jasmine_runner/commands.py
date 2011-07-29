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


def run_specs(path, browser_driver='webdriver.firefox'):
    print
    print 'Using %s as runner and %s as webdriver.' % (path, browser_driver)

    browser = Browser(browser_driver)
    browser.visit(path)

    Extractor = filter(lambda e: e.is_it_me(browser), [JExtractor, QExtractor])[0]

    extractor = Extractor(browser)
    extractor.wait_till_finished_and_then(print_result)

    browser.quit()

    return extractor.failures_number


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

