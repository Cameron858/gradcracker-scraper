from bs4 import BeautifulSoup

# div class="tw-flex tw-p-4" is each posting 'block'
# div class="tw-w-3/5 tw-pr-4 tw-space-y-2" is the actual job posting
# div class="tw-flex tw-flex-col tw-w-2/5 tw-pl-4 tw-border-l-2 tw-border-gray-100"

# opens the html file from local dir
with open('Mechanical_Manufacturing Engineering Graduate Jobs in North West _ Gradcracker - Careers for STEM '
          'Students.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    for posting in soup.find_all('div', class_="tw-flex tw-p-4"):
        j = posting.find_all('div', class_="tw-w-3/5 tw-pr-4 tw-space-y-2")
        for job in j:
            job_title = job.a.text.strip()
            job_info = job.ul.text
            job_salary = job.ul.text.splitlines()[1][1:]
            job_location = job.ul.text.splitlines()[2]
            job_accepting = job.ul.text.splitlines()[3]
            job_deadline = job.ul.text.splitlines()[-1]

        #   print(f'Title: {job_title} Salary: {job_salary} Location: {job_location} Requirements: {job_accepting}'
        #         f' Deadline: {job_deadline}')

        im = posting.find_all('div', class_="tw-flex tw-flex-col tw-w-2/5 tw-pl-4 tw-border-l-2 tw-border-gray-100")
        for logo in im:
            job_company = logo.a.img['alt']

