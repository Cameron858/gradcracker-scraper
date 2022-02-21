import re


def filter_salary_types(salary):
    # salary is expected to be a single string passed into this function

    # expected types of salaries from gradcracker - testing
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

    # this hurts to know I wrote this
    # TODO doesnt filter 'Competitive+bonus' types to 'Competitive' etc

    # does it start with a salary?
    if re.match("[€£][0-9]+", salary):
        salary = salary[0:7]
    else:
        # remove "up to" types
        if re.findall("^Up to", salary):
            salary = salary[6:]
        else:
            # remove text from salaries
            if re.findall("[£|€]", salary):
                idx = re.search("[£]", salary).start()
                salary = salary[idx:]
            else:
                pass

    return salary


def filter_location_types(location):
    # location is expected to be a single string
    # func filters down locations into more manageable data

    # list of example locations from gradcracker
    location_tests = [
        'Aberdeen',
        'Aberdeen, Perth, Glasgow, Cumbernauld (Glasgow) and Inverness',
        'Bad Hersfeld, Germany',
        'Abingdon (Oxfordshire)',
        'Basingstoke, Hampshire',
        'Bath, Leeds and Manchester',
        'Belfast, Birmingham, Bristol, Cheltenham, Dublin, Ireland, London and Manchester',
        'Blaydon-On-Tyne (Newcastle)',
        'Cardiff/Hybrid',
        'Hebburn (near Newcastle)',
        'I10 Office (Wolverhampton)',
        'UK + International',
    ]

    return location
