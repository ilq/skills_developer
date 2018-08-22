from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup


def fetch_pages_moikrug(size: int=10):
    url_moikrug = 'https://moikrug.ru/vacancies?page={}&type=all'  # type: str
    urls = [url_moikrug.format(i) for i in range(1, size+1)]  # type: List[str]
    raw_pages = []
    for url_page in urls:
        try:
            response = requests.get(url_page)
        except requests.exceptions.RequestException as e:
            print(e)
            continue
        if response.status_code == 200:
            raw_pages.append(response.text)
    return raw_pages


def parse_vacancy_from_job_element(job_element):
    title_element = job_element.find('div', class_='title')
    date_element = job_element.find('span', class_='date')
    specialization_element = job_element.find('div', class_='specialization')
    specialization_skills_elements = specialization_element.find_all(
        'a', class_='skill'
    )
    specialization_skills = [
        skill_element.string for skill_element in specialization_skills_elements
    ]
    skills_elements = job_element.find_all('a', class_='skill')
    skills = [
        skill_element.string for skill_element in skills_elements
    ]
    vacancy = {
        'title': title_element.string,
        'date': date_element.string,
        'specialization_skills': specialization_skills,
        'skills': skills,
    }
    return vacancy


def parse_vacancies_from_raw_page_moikrug(raw_page: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(raw_page, 'html.parser')
    job_elements = soup.find_all('div', class_='job')
    vacancies = [
        parse_vacancy_from_job_element(job_element)
        for job_element in job_elements
    ]
    return vacancies


def parse_vacancies_from_raw_pages_moikrug(raw_pages: List[str]) -> List[Dict]:
    vacancies = []
    for raw_page in raw_pages:
        vacancies += parse_vacancies_from_raw_page_moikrug(raw_page)
    return vacancies
