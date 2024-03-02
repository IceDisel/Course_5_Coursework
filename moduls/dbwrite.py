import psycopg2
from psycopg2 import sql


class DBWrite:
    def __init__(self, database_name: str, params: dict) -> None:
        """
        Инициализация БД
        :param database_name: Имя БД
        :param params: Параметры подключения
        """
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(sql.SQL(
                """SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
                WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();"""),
                (database_name,))
            cur.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(database_name)))
            cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(database_name)))
        except psycopg2.Error as e:
            print(f"Ошибка при удалении/создании базы данных: {e}")
        finally:
            cur.close()
            conn.close()

        self.conn = psycopg2.connect(dbname=database_name, **params)

        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers (
                            employer_id INTEGER PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            type VARCHAR(255),
                            description TEXT,
                            site_url VARCHAR(255))""")

        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            salary VARCHAR(25),
                            url VARCHAR(255),
                            requirement TEXT,
                            employer_id INT REFERENCES employers(employer_id))""")

        self.conn.commit()
        # self.conn.close()

    def __del__(self) -> None:
        try:
            self.conn.close()
        except AttributeError:
            pass

    def write_db(self, employer: dict, vacancies: list) -> None:
        """
        Метод записи данных работодателей и вакансий в БД.
        :param employer: Данные о работодателе
        :param vacancies: Данные о вакансиях
        :return: None
        """
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO employers VALUES (%s, %s, %s, %s, %s)", (
                employer["employer_id"], employer["name"], employer["type"], employer["description"],
                employer["site_url"]))

            for vacancy in vacancies:
                cur.execute("""INSERT INTO vacancies (name, salary, url, requirement, employer_id)
                VALUES (%s, %s, %s, %s, %s)""", (vacancy["name"], vacancy["salary"], vacancy["url"],
                                                 vacancy["requirement"], vacancy["employer_id"]))

        self.conn.commit()
