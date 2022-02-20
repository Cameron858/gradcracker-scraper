import re


def test():

    salary_tests = [
        '£30,000',
        '€32,000',
        '£20,000-£30,000',
        '£20,000 - £30,000',
        '£20,000-£30,000 rising after programme completion',
        '£22,000 rising to £30,000 after completion of graduate scheme'
    ]

    for w in salary_tests:
        # print(re.split('-', w))
        pass

    for x in salary_tests:
        print(bool(re.match("[£][0-9]+[,][0-9]+[ |-]+[£]", x)))


test()
