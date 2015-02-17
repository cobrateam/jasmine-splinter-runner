#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

from jasmine_runner.extractors import BaseExtractor, class_xpath_to_css


class Extractor(BaseExtractor):

    def __init__(self, browser):
        super(Extractor, self).__init__(browser)

    @staticmethod
    def is_it_me(browser):
        if browser.is_element_present_by_id('mocha'):
            return True

    def has_finished(self):
        return self.browser.evaluate_script(
            'window.mocha !== undefined && !window.mocha.suite.pending')

    def has_failed(self):
        self.failures_number > 0

    @property
    def failures_number(self):
        return int(self.browser.find_by_id('mocha-stats').first.find_by_css('.failures').first.find_by_tag('em').first.text)

    @property
    def description(self):
        return "Mocha"

    def get_failures(self):
        '''
            this function returns an array with the following structure:
            [{'title of test suite':
                [{'title of nested test suite':
                    [{'spec description': ['spec error message']}, ...]
                , ...]
            , ...]
        '''

        def parent_suite(test):
            parents = test.find_by_xpath("ancestor::li[@class='suite']")
            if parents:
                return parents.first

        def treat_failure(failure):
            title = failure.find_by_xpath("h1|h2|h3|h4|h5").first.text
            content = failure.find_by_css(".error").text
            return {title: [content]}

        def treat_suite(suite):
            failures = suite.find_by_css(".fail")
            if not failures:
                return None
            direct_failures = [
                t for t in failures
                if parent_suite(t)._element._id == suite._element._id]
            subsuites = [treat_suite(s) for s in suite.find_by_css(".suite")]
            subsuites = [s for s in subsuites if s is not None]
            title = suite.find_by_xpath("h1|h2|h3|h4|h5").first.text
            subsuites.extend([treat_failure(f) for f in direct_failures])
            if subsuites:
                return {title: subsuites}

        suites = self.browser.find_by_id('mocha-report').find_by_css(".suite")
        direct_suites = [s for s in suites if parent_suite(s) is None]

        res = [treat_suite(s) for s in direct_suites]
        return [r for r in res if r is not None]
