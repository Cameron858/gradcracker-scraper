import math
import requests
from bs4 import BeautifulSoup
from util.general_util import get_job_info


def get_page_count(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    results_list = soup.find_all("ul", class_="breadcrumb")
    results_string = results_list[0].find_all("li")[2].text.split()
    number_of_pages = math.ceil(int(results_string[4].replace(',', "")) / int(results_string[2]))
    print(f'There are {number_of_pages} pages available.')

    return number_of_pages


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
