#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

from jasmine_runner.extractors import BaseExtractor, class_xpath_to_css


class Extractor(BaseExtractor):

    @staticmethod
    def is_it_me(browser):
        return browser.is_element_present_by_css('.jasmine_reporter')

    def has_finished(self):
        return not self.browser.is_text_present("Running...")

    def has_failed(self):
        runner_div = self.browser.find_by_css('.runner').first
        return not 'passed' in runner_div['class']

    @property
    def failures_number(self):
        if hasattr(self, '_failures'):
            return self._failures

        if self.has_failed():
            self._failures = int(re.search(r'(\d+)\s*failure', self.description).group(1))
        else:
            self._failures = 0

        return self._failures

    @property
    def description(self):
        if hasattr(self, '_description'):
            return self._description

        self._description = self.browser.find_by_css(".runner .description").first.text
        return self._description

    def get_failures(self):
        rootDescribes = self.browser.find_by_xpath('//*%s/*%s%s' % (
            class_xpath_to_css('jasmine_reporter'),
            class_xpath_to_css('suite'),
            class_xpath_to_css('failed'),
        ))

        specs = []

        def traverse(describes, specs):
            for describe in describes:
                desc = describe.find_by_css('.description')
                spec = {}
                children = spec[desc.first.text] = []
                specs.append(spec)
                
                if 'suite' in describe['class']:
                    traverse(
                        describe.find_by_xpath('*%s' % class_xpath_to_css('failed')),
                        children
                    )
                elif 'spec' in describe['class']:
                    children.extend(map(lambda el: el.text, describe.find_by_css('.resultMessage')))

        traverse(rootDescribes, specs)

        return specs

