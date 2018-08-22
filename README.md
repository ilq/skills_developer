# skills_developer
Скрипт считает количество требуемых навыков с moikrug.


# Установка

```bash
git clone https://github.com/ds-vologdin/skills_developer.git
cd skills_developer
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

# Запуск

```bash
source env/bin/activate
python skills_analyze.py --page-size 3 --category python --top-skills 50
```

```bash
python skills_analyze.py -h
usage: skills_analyze.py [-h] [--page-size PAGE_SIZE]
                         [--top-skills TOP_SKILLS] [--category {all,python}]

Приложение для парсинга вакансий и поиска актуальных навыков

optional arguments:
  -h, --help            show this help message and exit
  --page-size PAGE_SIZE
                        Количество анализируемых страниц на moikrug
  --top-skills TOP_SKILLS
                        Вывести TOP-SKILLS самых частых навыков. Если --top-
                        skills 0 будут показаны все навыки. Поумолчанию --top-
                        skills 20.
  --category {all,python}
                        Параметр для сужения окна поиска

```
