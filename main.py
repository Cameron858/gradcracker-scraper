# TODO
#   make main and get page count take url as karg
#   handling for multiple opportunities, atm I just ignore them and take all other data
#   some sort of visualisation, folium module to visualise could be very cool tbh

from time import sleep
from random import randint
from datetime import date
from util.web_scraping_util import get_page_count, parse_page_from_url
from util.general_util import export_df_as_csv


def main():

    print('Starting...')
    url_all_discs = "https://www.gradcracker.com/search/all-disciplines/" \
                    "engineering-graduate-jobs?order=deadlines&page={}"

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
    export_df_as_csv(total_listings, cols, 'eng-jobs-{}'.format(date.today()), save_state=True)


if __name__ == '__main__':
    main()
