#-*- encoding: utf8 -*-

from termcolor import colored
from jasmine_extractor import extract_failures


def print_errors(browser, output):
    print
    print len(output) * "-"
    print colored(output, 'yellow')
    print len(output) * "-"
    print

    print format_errors(extract_failures(browser))
    print


def format_errors(errors):
    ret = []
    for error in errors:
        ret.extend(_print(error, [], 0));
    return '\n'.join(ret)


def _print(obj, buffer, level):
    for title, desc in obj.iteritems():
        buffer.append((level * 2 * ' ') + title);
        if desc and isinstance(desc[0], basestring):
            for err in desc:
                buffer.append(colored(u'%s  ✗ %s' % ((level * 2 * u' '), err), 'red'));
        else:
            level += 1;
            for suite in desc:
                _print(suite, buffer, level);

    return buffer

        #print
        #suite = browser.find_by_css(".jasmine_reporter .suite.failed .description").first.text
        #print colored("Suite: " + suite)
        #specs = browser.find_by_css(".jasmine_reporter .suite.failed .suite.failed .spec.failed")
        #for spec in specs:
            #spec_description = spec.find_by_css(".description").first
            #print colored("   Spec: " + spec_description.text)
            #result_messages = spec.find_by_css(".messages .resultMessage")
            #for result_message in result_messages:
                #print colored("        Test: " + result_message.text, color)

