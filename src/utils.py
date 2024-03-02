import re

from moduls.api_hh import HeadHunterAPI


def get_vacancies_by_employer(employer_id: str) -> list:
    """
    Функция поиска вакансий на HH.ru по ID работодателя.
    :param employer_id: ID работодателя.
    :return: Список найденных вакансий.
    """
    hh_api = HeadHunterAPI(employer_id)
    data_hh = hh_api.get_vacancies_by_employer()

    list_search = []

    for item in data_hh:
        try:
            list_search.append({
                'name': item['name'],
                'salary': item['salary']['from'],
                'url': item['alternate_url'],
                'requirement': clean_text(item['snippet']['requirement']),
                'employer_id': int(item['employer']['id'])
            })
        except TypeError:
            pass

    return list_search


def get_employer_info(employer_id: str) -> dict:
    """
    Получение информации об организации работодателя.
    :param employer_id: ID работодателя.
    :return: Информация об организации работодателя
    """
    data_hh = HeadHunterAPI(employer_id).get_employer_info()

    dict_employer = {
        'employer_id': int(data_hh['id']),
        'name': data_hh['name'],
        'type': data_hh['type'],
        'description': clean_text(data_hh['description']),
        'site_url': data_hh['site_url']
    }
    return dict_employer


def clean_text(text: str) -> str:
    """
    Функция форматирования текста (удаление тегов и символов)
    :param text: Строка
    :return: Форматированная строка
    """
    # Удаление HTML-тегов
    text = re.sub('<.*?>', ' ', text)
    # Замена неразрывных пробелов на обычные
    text = text.replace('\xa0', ' ')
    # Удаление лишних пробелов
    text = re.sub(' +', ' ', text)
    return text.strip()
