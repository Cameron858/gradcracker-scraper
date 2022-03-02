import pandas as pd
from util.data_filters_util import filter_salary_types


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
