import psycopg2


class DBManager:
    """
    Класс получения данных из БД.
    """
    def __init__(self, database_name: str, params: dict) -> None:
        try:
            self.conn = psycopg2.connect(dbname=database_name, **params)
        except psycopg2.OperationalError:
            raise AttributeError

    def __del__(self) -> None:
        try:
            self.conn.close()
        except AttributeError:
            pass

    def get_companies_and_vacancies_count(self) -> list:
        """
        Метод получает список всех компаний и количество вакансий у каждой компании.
        :return: Список результатов запроса
        """
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employers.name, COUNT(vacancies.vacancy_id) AS vacancy_count
                            FROM employers
                            JOIN vacancies USING(employer_id)
                            GROUP BY employers.name;""")

            return list(cur)

    def get_all_vacancies(self) -> list:
        """
        Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return: Список результатов запроса
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT e.name AS company_name, v.name AS vacancy_name, v.salary, v.url
                    FROM employers e
                    JOIN vacancies v USING(employer_id);""")

            return list(cur)

    def get_avg_salary(self) -> float:
        """
        Метод получает среднюю зарплату по вакансиям.
        :return: Результат запроса
        """
        with self.conn.cursor() as cur:
            cur.execute("""SELECT AVG(CAST(salary AS NUMERIC)) AS average_salary
                            FROM vacancies;""")
            for row in cur:
                avg_vacancies = row[0]

        return round(avg_vacancies, 2)

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Список результатов запроса
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT v.name AS vacancy_name, v.salary, e.name AS company_name
                    FROM vacancies v
                    JOIN employers e USING(employer_id)
                    WHERE CAST(v.salary AS NUMERIC) > (SELECT AVG(CAST(salary AS NUMERIC)) FROM vacancies);""")

            return list(cur)

    def get_vacancies_with_keyword(self, search_word: str) -> list:
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :param search_word:
        :return: Список результатов запроса
        """
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM vacancies WHERE name ILIKE '%{search_word}%' OR requirement ILIKE '%{search_word}%';")

            return list(cur)
