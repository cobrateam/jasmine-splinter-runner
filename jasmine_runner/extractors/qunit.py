#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jasmine_runner.extractors import BaseExtractor, class_xpath_to_css


class Extractor(BaseExtractor):

    @staticmethod
    def is_it_me(browser):
        return browser.is_element_present_by_id('qunit-header')

    def has_finished(self):
        return self.browser.is_element_present_by_id('qunit-testresult')

    def has_failed(self):
        banner = self.browser.find_by_id('qunit-banner')
        return 'qunit-fail' in banner['class']

    @property
    def failures_number(self):
        if hasattr(self, '_failures'):
            return self._failures

        self._failures = int(self.browser.find_by_css('#qunit-testresult .failed').text)
        return self._failures

    @property
    def description(self):
        if hasattr(self, '_description'):
            return self._description

        self._description = self.browser.find_by_id('qunit-testresult').text
        return self._description

    def get_failures(self):

        specs = []

        fail_container = self.browser.find_by_id('qunit-tests')
        fail_suites = fail_container.find_by_xpath('*%s' % class_xpath_to_css('fail'))

        for suite in fail_suites:
            suite_description_node = suite.find_by_tag('strong').first
            # hack to make message "pickable"
            # some drivers (selenium) do not allow to get the text if the element is not visible
            suite_description_node.click()
            description = suite_description_node.text

            fail_messages = map(lambda el: el.text, suite.find_by_xpath('ol/li%s' % class_xpath_to_css('fail')))

            specs.append({
                description: fail_messages
            })

        return specs


