import re


def test():

    # expected types of salaries from gradcracker
    salary_tests = [
        '£30,000',
        '€32,000',
        '£20,000-£30,000',
        '£20,000 - £30,000',
        '£30,973 to £38,237',
        '£20,000-£30,000 rising after programme completion',
        '£22,000 rising to £30,000 after completion of graduate scheme',
        '£24,500 after training',
        '£25,714 (nationally) or £32,157 (inner London)',
        '£26,750 + £1,500 welcome bonus',
        '£26,750 plus £1,500 welcome bonus',
        '£27,000, rising to around £33,000 after two years',
        '£45,000 - £50,000 salary + £2,000 - £5,000 sign on bonus',
        'Competitive salary',
        'Free training then £30,000',
        'Up to £23,655'
    ]

    for x in salary_tests:
        print(bool(re.match("[£][0-9]+[,][0-9]+[ |-]+[£]", x)))
        print(re.findall(".......*-", x))


test()
