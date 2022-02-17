# TODO
#  save data as a csv (do i want seperate ones each day?)
#  handling for multiple opportunities, atm I just ignore them and take all other data
#  some sort of visualisation??
#  folium module to visualise could be very cool tbh

from bs4 import BeautifulSoup
import requests


def main():
    soup = BeautifulSoup(requests.get(
        "https://www.gradcracker.com/search/mechanical-manufacturing/engineering-graduate-jobs-in-north-west"
        "?order=deadlines").content, "html.parser")

    # div class="tw-flex tw-p-4" is each posting 'block'
    # div class="tw-w-3/5 tw-pr-4 tw-space-y-2" is the actual job posting
    # div class="tw-flex tw-flex-col tw-w-2/5 tw-pl-4 tw-border-l-2 tw-border-gray-100"

    postings = soup.find_all('div', class_="tw-flex tw-p-4")
    print(f'There are {len(postings)} jobs available\n')
    for posting in postings:
        # Company name can be found in the alt text for the company's logo
        alt_image = posting.find('div', class_="tw-flex tw-flex-col tw-w-2/5 tw-pl-4 tw-border-l-2 "
                                               "tw-border-gray-100")
        job_company = alt_image.a.img['alt']

        # the rest of the relavent infomation can be found in the main posting
        job = posting.find('div', class_="tw-w-3/5 tw-pr-4 tw-space-y-2")
        job_title = job.a.text.strip()
        job_info = job.ul.text
        job_salary = job.ul.text.splitlines()[1][1:]
        job_location = job.ul.text.splitlines()[2]
        job_accepting = job.ul.text.splitlines()[3]
        job_deadline = job.ul.text.splitlines()[-1]

        print(f'Title: {job_title} Company: {job_company} Salary: {job_salary} Location: {job_location}'
              f'Requirements: {job_accepting} Deadline: {job_deadline}')


if __name__ == '__main__':
    main()
