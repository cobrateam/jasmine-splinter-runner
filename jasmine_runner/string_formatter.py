from termcolor import colored

def format_exit(browser, output, color):
        print

        print len(output) * "-"
        print colored(output, color)
        print len(output) * "-"

        print

        suite = browser.find_by_css(".jasmine_reporter .suite.failed .description").first.text
        print colored("Suite: " + suite)

        specs = browser.find_by_css(".jasmine_reporter .suite.failed .suite.failed .spec.failed")

        for spec in specs:
            spec_description = spec.find_by_css(".description").first
            print colored("   Spec: " + spec_description.text)
            result_messages = spec.find_by_css(".messages .resultMessage")

            for result_message in result_messages:
                print colored("        Test: " + result_message.text, color)
