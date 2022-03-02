import re


def filter_salary_types(salary):
    # salary is expected to be a single string passed into this function

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
