#!/usr/bin/env python
# -*- coding:utf-8 -*-

def class_xpath_to_css(_class):
    return '[contains(concat(" ",normalize-space(@class)," ")," %s ")]' % _class


class BaseExtractor(object):

    def __init__(self, browser):
        self.browser = browser

    def wait_till_finished_and_then(self, function):
        while not self.has_finished():
            pass
        function(self)

    def get_failures(self):
        '''
            this function returns an array with the following structure:
            [{'title of test suite':
                [{'title of nested test suite':
                    [{'spec description': ['spec error message']}, ...]
                , ...]
            , ...]
        '''
        raise NotImplemented


