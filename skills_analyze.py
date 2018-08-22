from typing import List, Dict
from collections import Counter
from texttable import Texttable

from moikrug import fetch_pages_moikrug
from moikrug import parse_vacancies_from_raw_pages_moikrug


def calc_frequency_skills(vacancies):
    skills = []
    for vacancy in vacancies:
        skills += vacancy.get('skills', [])
    return Counter(skills)


def output_frequency_skills(frequency_skills):
    # Инициализируем таблицу на печать
    table = Texttable()
    table.set_cols_align(['c', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(['Навык', 'Как часто требуется'])
    for frequency_skill in frequency_skills.most_common():
        table.add_row(frequency_skill)
    # Прорисовываем таблицу
    print(table.draw())


def main():
    raw_pages = fetch_pages_moikrug(size=5)  # type: List[str]
    vacancies = parse_vacancies_from_raw_pages_moikrug(raw_pages)  # type: List[Dict]
    frequency_skills = calc_frequency_skills(vacancies)
    print('Проанализировано {} вакансий. Повстречали {} навыков.'.format(
        len(vacancies), len(frequency_skills)
    ))
    output_frequency_skills(frequency_skills)


if __name__ == '__main__':
    main()
