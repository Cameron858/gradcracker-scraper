# TODO
#  allow custom search criteria
#  handling for multiple opportunities, atm I just ignore them and take all other data
#  some sort of visualisation??
#  folium module to visualise could be very cool tbh

import requests
import pandas as pd
from time import sleep
from random import randint
from datetime import date
from bs4 import BeautifulSoup
from gradcracker_scraper_util import filter_salary_types, export_df_as_csv, get_page_count


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

    # check is posting has stated discipline
    if job.find('div', class_="tw-text-xs tw-font-bold tw-text-gray-800") is not None:
        job_discipline = job.find('div', class_="tw-text-xs tw-font-bold tw-text-gray-800").text
    else:
        job_discipline = 'N/A'

    # returns list
    return [job_discipline, job_title, job_company, job_salary, job_location, job_accepting, job_deadline]


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


def main():

    print('Starting...')
    url_all_discs = "https://www.gradcracker.com/search/all-disciplines/engineering-graduate-jobs?order=deadlines&page={}"

    pages = get_page_count(url_all_discs.format(1))
    total_listings = []     # to be used to store the total listings
    cols = ['Discipline', 'Job title', 'Company', 'Salary', 'Location', 'Accepting', 'Deadline']

    for page_number in range(1, pages + 1):

        print(f'Processing page {page_number} out of {pages}')
        sleep(randint(1, 2))        # prevent ip timeouts

        page_listings = parse_page_from_url(url_all_discs.format(page_number))

        # unpack page listings as separate jobs. not great but it works for now
        for p in page_listings:
            total_listings.append(p)

    # saves as csv
    total_listings_df = pd.DataFrame(total_listings, columns=cols)
    export_df_as_csv(total_listings_df, cols, 'eng-jobs-{}'.format(date.today()), save_state=True)


if __name__ == '__main__':
    main()
