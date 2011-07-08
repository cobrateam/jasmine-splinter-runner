
def class_xpath_to_css(_class):
    return '[contains(concat(" ",normalize-space(@class)," ")," %s ")]' % _class

def extract_failures(browser):
    rootDescribes = browser.find_by_xpath('//*%s/*%s%s' % (
        class_xpath_to_css('jasmine_reporter'),
        class_xpath_to_css('suite'),
        class_xpath_to_css('failed'),
    ))
    specs = []

    def traverse(describes, specs):
        for describe in describes:

            desc = describe.find_by_xpath('*%s' % class_xpath_to_css('description'))
            spec = {}
            children = spec[desc.first.text] = []
            specs.append(spec)

            if 'suite' in describe['class']:
                traverse(
                    describe.find_by_xpath(
                        '*%s%s | *%s%s' % (
                            class_xpath_to_css('spec'),
                            class_xpath_to_css('failure'),
                            class_xpath_to_css('suite'),
                            class_xpath_to_css('failure'),
                        )
                    ),
                    children
                )
            elif 'spec' in describe['class']:
                children.extend(map(describe.find_by_xpath('*%s' % class_xpath_to_css('resultMessage')), lambda el: el.text))

    traverse(rootDescribes, specs)

    return specs

