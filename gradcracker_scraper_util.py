import re
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup


def export_df_as_csv(total_job_listings_list, cols, filename, save_state=None):
    if save_state is None:
        print("Save state not given.")
    elif save_state:
        # append data list to pandas dataframe, save as .csv
        # csv encoding is essential to ignore strange errors
        df = pd.DataFrame(total_job_listings_list, columns=cols)
        df.to_csv('{}.csv'.format(filename), index=False, encoding='utf-8-sig')
        print("The job listings have been saved")
    else:
        print(f"The job listings have not been saved, save_state = {save_state}")


def get_page_count(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    results_list = soup.find_all("ul", class_="breadcrumb")
    results_string = results_list[0].find_all("li")[2].text.split()
    number_of_pages = math.ceil(int(results_string[4].replace(',', "")) / int(results_string[2]))
    print(f'There are {number_of_pages} pages available.')

    return number_of_pages


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
