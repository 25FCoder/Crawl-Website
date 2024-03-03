import requests
import pandas as pd
from bs4 import BeautifulSoup


def input_keywords():
    keywords = input("Input keywords: ")
    keywords = keywords.replace(" ", "%20")
    return keywords


def get_response_keywords(keywords):
    print('Call api keywords')
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location=Vietnam&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&start=1"
    response = requests.get(url)
    return response


def get_job_links(response):
    print('Get job links')
    btf_soup = BeautifulSoup(response.content, "html.parser")
    list_jobs = btf_soup.findAll("li")
    job_links = []
    for job in list_jobs:
        job_link = (
            job.find("a", class_="base-card__full-link").get("href")
            if job.find("a", class_="base-card__full-link")
            else ""
        )
        job_links.append(job_link)
    return job_links


def get_data_job(job_link):
    print(f'Get data job from {job_link}')
    response = requests.get(job_link)
    soup = BeautifulSoup(response.content, "html.parser")
    job_title = (
        soup.find("h1", class_="top-card-layout__title").text
        if soup.find("h1", class_="top-card-layout__title")
        else None
    )
    org_name = (
        soup.find("a", class_="topcard__org-name-link").text
        if soup.find("a", class_="topcard__org-name-link")
        else None
    )
    location = (
        soup.find("span", class_="topcard__flavor--bullet").text
        if soup.find("span", class_="topcard__flavor--bullet")
        else None
    )
    job_description = (
        soup.find("div", class_="show-more-less-html__markup").text
        if soup.find("div", class_="show-more-less-html__markup")
        else None
    )
    description_job_creteria_list = soup.findAll(
        "span", class_="description__job-criteria-text"
    )
    seniority_level = (
        description_job_creteria_list[0].text
        if description_job_creteria_list
        else None
    )
    employment_type = (
        description_job_creteria_list[1].text
        if description_job_creteria_list
        else None
    )
    job_function = (
        description_job_creteria_list[2].text
        if description_job_creteria_list
        else None
    )
    industries = (
        description_job_creteria_list[3].text
        if description_job_creteria_list
        else None
    )

    data_job = dict(
        Title=job_title,
        Organization=org_name,
        Location=location,
        Description=job_description,
        Seniority_level=seniority_level,
        Employment_type=employment_type,
        Job_function=job_function,
        Industries=industries,
        Job_link=job_link,
    )
    return data_job


def write_to_excel(data_jobs):
    print("Writing to Excel...")
    df_jobs = pd.DataFrame(data_jobs)
    df_jobs.to_excel("Linkedin_job.xlsx", index=False)


keywords = input_keywords()
response = get_response_keywords(keywords)
job_links = get_job_links(response)
data_jobs = []
for job_link in job_links:
    data_job = get_data_job(job_link)
    data_jobs.append(data_job)

write_to_excel(data_jobs)
print("Crawl data jobs linkedin successfully!")