import asyncio
from typing import List, Dict, Any

import aiohttp
import requests
from bs4 import BeautifulSoup


async def fetch_page_moikrug_async(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                response_text = await response.text()
            except aiohttp.ClientResponseError:
                return ''
            return response_text


def _fetch_pages_moikrug_async(urls: List[str]) -> List[str]:
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(fetch_page_moikrug_async(url))
        for url in urls
    ]
    done, _ = loop.run_until_complete(asyncio.wait(tasks))
    return [fut.result() for fut in done]


def get_url_for_type_vacancies(type_vacancies: str = 'all') -> str:
    url_moikrug_dict = {
        'all': 'https://moikrug.ru/vacancies?page={}&type=all',
        'python': ('https://moikrug.ru/vacancies?page={}'
                   '&skills%5B%5D=446&type=all'),
    }

    if type_vacancies not in url_moikrug_dict:
        type_vacancies = 'all'

    return url_moikrug_dict[type_vacancies]


def _fetch_pages_moikrug(urls: List[str]) -> List[str]:
    raw_pages = []

    for url_page in urls:
        try:
            response = requests.get(url_page)
        except requests.exceptions.RequestException as exceptions_instance:
            print(exceptions_instance)
            continue

        if response.status_code == 200:
            raw_pages.append(response.text)

    return raw_pages


def fetch_pages_moikrug(size: int = 10, category: str = 'all',
                        is_no_async: bool = False) -> List[str]:
    url_moikrug = get_url_for_type_vacancies(category)  # type: str
    urls = [url_moikrug.format(i) for i in range(1, size+1)]  # type: List[str]
    raw_pages = (_fetch_pages_moikrug(urls) if is_no_async
                 else _fetch_pages_moikrug_async(urls))
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


def parse_vacancies_from_raw_page_moikrug(
    raw_page: str
    ) -> List[Dict[str, Any]]:
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
