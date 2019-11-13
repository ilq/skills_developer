from typing import List, Dict
import argparse
from collections import Counter
from texttable import Texttable

from moikrug import fetch_pages_moikrug
from moikrug import parse_vacancies_from_raw_pages_moikrug


def parse_argv():
    parser = argparse.ArgumentParser(
        description=('Приложение для парсинга вакансий и поиска '
                     'актуальных навыков')
    )
    parser.add_argument(
        '--page-size', type=int, default=10,
        help='Количество анализируемых страниц на moikrug. Поумолчанию 10'
    )
    parser.add_argument(
        '--top-skills', type=int, default=20,
        help=('Вывести TOP-SKILLS самых частых навыков. Если --top-skills 0 '
              'будут показаны все навыки. Поумолчанию --top-skills 20.')
    )
    parser.add_argument(
        '--category', choices=['all', 'python'], default='all',
        help='Параметр для сужения окна поиска'
    )
    parser.add_argument(
        '--no-async', action='store_true',
        help='Асинхронные запросы. Поумолчанию: True'
    )
    return parser.parse_args()


def calc_frequency_skills(vacancies):
    skills = []

    for vacancy in vacancies:
        skills += vacancy.get('skills', [])

    return Counter(skills)


def output_frequency_skills(frequency_skills, top_size=None):
    # Инициализируем таблицу на печать
    table = Texttable()
    table.set_cols_align(['c', 'c', 'c'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(['#', 'Навык', 'Как часто требуется'])

    for numb, frequency_skill in \
        enumerate(frequency_skills.most_common(top_size)):
        table.add_row((numb, *frequency_skill))

    # Прорисовываем таблицу
    print(table.draw())


def main():
    argv = parse_argv()
    skills_top_size = argv.top_skills if argv.top_skills > 0 else None
    raw_pages = fetch_pages_moikrug(
        argv.page_size, argv.category, argv.no_async
    )  # type: List[str]
    vacancies = parse_vacancies_from_raw_pages_moikrug(
        raw_pages
    )  # type: List[Dict]
    frequency_skills = calc_frequency_skills(vacancies)
    print(f'Посмотрели {len(raw_pages)} страниц. '
          f'Проанализировано {len(vacancies)} вакансий. '
          f'Повстречали {len(frequency_skills)} навыков.')
    output_frequency_skills(frequency_skills, skills_top_size)


if __name__ == '__main__':
    main()
