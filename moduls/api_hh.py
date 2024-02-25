from typing import Any

import requests


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter.
    """

    def __init__(self, employer_id: str) -> None:
        """
        Инициализация полей для API.
        :param employer_id: ID работодателя.
        """
        self.__employer_id = employer_id

    def get_vacancies_by_employer(self):
        """
        Получение списка вакансий конкретного работодателя.
        :return: Список вакансий
        """

        url = 'https://api.hh.ru/vacancies'

        params = {
            'employer_id': self.__employer_id,
            'per_page': 100,  # количество вакансий на одной странице
            'page': 0  # номер страницы
        }

        response = requests.get(url, params=params)
        data = response.json()

        return data['items']

    def get_employer_info(self) -> Any:
        """
        Получение информации об организации работодателя.
        :return: Информация об организации работодателя
        """
        url = f'https://api.hh.ru/employers/{self.__employer_id}'
        response = requests.get(url)
        data = response.json()

        return data
