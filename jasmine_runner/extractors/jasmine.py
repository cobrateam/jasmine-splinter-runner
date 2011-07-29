import re


def class_xpath_to_css(_class):
    return '[contains(concat(" ",normalize-space(@class)," ")," %s ")]' % _class

class Extractor(object):

    def __init__(self, browser):
        self.browser = browser

    @property
    def failures_number(self):
        if hasattr(self, '_failures'):
            return self._failures

        runner_div = self.browser.find_by_css('.runner').first
        if 'passed' in runner_div['class']:
            self._failures = 0
        else:
            self._failures = int(re.search(r'(\d+)\s*failure', self.description).group(1))

        return self._failures

    @property
    def description(self):
        if hasattr(self, '_description'):
            return self._description

        self._description = self.browser.find_by_css(".runner .description").first.text
        return self._description

    def has_finished(self):
        return self.browser.is_text_present("Running...")

    def wait_till_finished_and_then(self, function):
        # maybe we can make this
        while self.has_finished():
            pass

        function(self)

    def get_failures(self):
        '''
            this function returns an array with the following structure:
            [{'title of test suite':
                [{'title of nested test suite':
                    [{'spec description': 'spec error message'}, ...]
                , ...]
            , ...]
        '''
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

