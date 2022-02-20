# TODO
#  loop through the disciplines and add as another category
#  allow custom search criteria
#  handling for multiple opportunities, atm I just ignore them and take all other data
#  some sort of visualisation??
#  folium module to visualise could be very cool tbh

import math
import requests
import pandas as pd
from time import sleep
from random import randint
from datetime import date
from bs4 import BeautifulSoup


def get_page_count():
    soup = BeautifulSoup(requests.get("https://www.gradcracker.com/search/all-disciplines/engineering-graduate-jobs"
                                      "?order=deadlines&page=1").content, "html.parser")
    results_list = soup.find_all("ul", class_="breadcrumb")
    results_string = results_list[0].find_all("li")[2].text.split()
    number_of_pages = math.ceil(int(results_string[4].replace(',', "")) / int(results_string[2]))

    return number_of_pages


def get_job_info(listing):
    # listing is of bs4 ResultSet type

    # Company name can be found in the alt text for the company's logo
    # div class="tw-flex tw-flex-col tw-w-2/5 tw-pl-4 tw-border-l-2 tw-border-gray-100" is the logo and company desc
    alt_image = listing.find('div', class_="tw-flex tw-flex-col tw-w-2/5 tw-pl-4 tw-border-l-2 "
                                           "tw-border-gray-100")
    job_company = alt_image.a.img['alt']

    # the rest of the relevant information can be found in the main posting
    # div class="tw-w-3/5 tw-pr-4 tw-space-y-2" is the actual job posting (left 'half' of posting block)
    job = listing.find('div', class_="tw-w-3/5 tw-pr-4 tw-space-y-2")
    job_title = job.a.text.strip()
    job_salary = filter_salary_types(job.ul.text.splitlines()[1])
    job_location = job.ul.text.splitlines()[2]
    job_accepting = job.ul.text.splitlines()[3]
    job_deadline = job.ul.text.splitlines()[-1]

    # returns list
    return [job_title, job_company, job_salary, job_location, job_accepting, job_deadline]


def parse_page_from_url(page_url):
    # data is list of job listings on page_url
    data = []

    soup = BeautifulSoup(requests.get(page_url).content, "html.parser")

    # div class="tw-flex tw-p-4" is each posting 'block' on gradcracker
    postings = soup.find_all('div', class_="tw-flex tw-p-4")
    print(f'There are {len(postings)} jobs available on this page')

    # list available jobs
    for posting in postings:
        job = get_job_info(posting)
        data.append(job)

    return data


def export_df_as_csv(total_job_listings_list, filename, save_state=None):
    if save_state is None:
        print("Save state not given.")
    elif save_state:
        # append data list to pandas dataframe, save as .csv
        # csv encoding is essential to ignore strange errors
        cols = ['Job title', 'Company', 'Salary', 'Location', 'Accepting', 'Deadline']
        df = pd.DataFrame(total_job_listings_list, columns=cols)
        df.to_csv('{}.csv'.format(filename), index=False, encoding='utf-8-sig')
        print("The job listings have been saved")
    else:
        print(f"The job listings have not been saved, save_state = {save_state}")


def main():

    print('Starting...')

    pages = get_page_count()
    total_listings = []     # to be used to store the total listings
    cols = ['Job title', 'Company', 'Salary', 'Location', 'Accepting', 'Deadline']

    for page_number in range(1, pages + 1):
        # TODO data needs to be concatenated to previous versions each iteration
        # append() adds lists to wrong dim -> size of (2,80,6) instead of (160,6)

        print(f'Processing page {page_number} out of {pages}')
        sleep(randint(1, 2))        # prevent ip timeouts

        page_listings = parse_page_from_url(("https://www.gradcracker.com/search/all-disciplines/engineering"
                                             "-graduate-jobs?order=deadlines&page={}").format(page_number))

        # unpack page listings as separate jobs. not great but it works for now
        for p in page_listings:
            total_listings.append(p)

    # saves as csv
    total_listings_df = pd.DataFrame(total_listings, columns=cols)
    export_df_as_csv(total_listings_df, 'eng-jobs-{}'.format(date.today()), save_state=True)


if __name__ == '__main__':
    main()
