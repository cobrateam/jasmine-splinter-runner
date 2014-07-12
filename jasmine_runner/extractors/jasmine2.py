#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

from jasmine_runner.extractors import BaseExtractor, class_xpath_to_css


class Extractor(BaseExtractor):
    _failure_re = re.compile(r'(\d+)\s*failures')
    _specs_re = re.compile(r'^(\d+)\s*specs,')

    @staticmethod
    def is_it_me(browser):
        return browser.is_element_present_by_css('.html-reporter')

    def has_finished(self):
        return self.browser.is_element_present_by_css('.results')

    def has_failed(self):
        bars = self.browser.find_by_xpath('//div%s/div%s/span%s' % (
            class_xpath_to_css('html-reporter'),
            class_xpath_to_css('alert'),
            class_xpath_to_css('bar'),
        ))
        return any(['failed' in bar['class'] for bar in bars])

    @property
    def failures_number(self):
        if hasattr(self, '_failures'):
            return self._failures

        if self.has_failed():
            self._failures = int(self._failure_re.search(
                self.description).group(1))
        else:
            self._failures = 0

        return self._failures

    @property
    def description(self):
        if hasattr(self, '_description'):
            return self._description

        bars = self.browser.find_by_xpath('//div%s/div%s/span%s' % (
            class_xpath_to_css('html-reporter'),
            class_xpath_to_css('alert'),
            class_xpath_to_css('bar'),
        ))

        bars = [bar for bar in bars
                if self._specs_re.match(bar.text) and not bar.text[0] == '0']
        if not bars:
            return "Jasmine 2"
        self._description = bars[0].text
        return self._description

    def get_failures(self):
        '''
            this function returns an array with the following structure:
            [{'title of test suite':
                [{'title of nested test suite':
                    [{'spec description': ['spec error message']}, ...]
                , ...]
            , ...]
        '''
        results = self.browser.find_by_xpath('//div%s/div%s' % (
            class_xpath_to_css('html-reporter'),
            class_xpath_to_css('results')
        ))
        failure_details = results.find_by_xpath('div%s/div%s' % (
            class_xpath_to_css('failures'),
            class_xpath_to_css('failed'),
        ))
        summaryRoots = results.find_by_xpath('div%s/*' % (
            class_xpath_to_css('summary'),
        ))
        detail_messages = {}
        for detail in failure_details:
            id = detail.find_by_xpath('div%s/a' % (
                class_xpath_to_css('description'),))[0]['href']
            messages = [m.text for m in detail.find_by_xpath('div%s/div%s' % (
                class_xpath_to_css('messages'),
                class_xpath_to_css('result-message')))]
            detail_messages[id] = messages
        specs = []

        def traverse(describes, specs):
            for describe in describes:
                if 'suite-detail' in describe['class']:
                    pass
                elif 'suite' in describe['class']:
                    desc = describe.find_by_xpath('*%s/a' % (
                        class_xpath_to_css('suite-detail'),)).first
                    # Strangely, text fails
                    desc = desc.text or desc.html
                    spec = {}
                    children = spec[desc] = []
                    traverse(describe.find_by_xpath('*'), children)
                    if children:
                        specs.append(spec)
                elif 'specs' in describe['class']:
                    failures = describe.find_by_xpath('*%s/a' % (
                        class_xpath_to_css('failed'),))
                    for failure in failures:
                        id = failure['href']
                        title = failure.text or failure.html
                        specs.append({title: detail_messages[id]})

        traverse(summaryRoots, specs)
        return specs
