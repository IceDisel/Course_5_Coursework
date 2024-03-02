from moduls.dbmanager import DBManager
from moduls.dbwrite import DBWrite
from src.config import config
from src.setting import LIST_EMPLOYERS
from src.utils import get_employer_info, get_vacancies_by_employer


def user_interface() -> None:
    params = config()
    try:
        db = DBManager('hh_ru', params)
    except AttributeError:
        print("\nБД не создана\nвыберете пункт 1 в главном меню для обновления БД\n")
    else:
        while True:
            print("\nПеречень операций БД:\n"
                  "  1 - получить список всех компаний и количество вакансий у каждой компании\n"
                  "  2 - получить список всех вакансий с указанием названия компании, названия вакансии,"
                  "зарплаты и ссылки на вакансию\n"
                  "  3 - получить среднюю зарплату по вакансиям\n"
                  "  4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                  "  5 - получить список всех вакансий, в требованиях которых содержится искомое слово\n"
                  "  0 - ВЫХОД")
            num_operation = int(input('Введите номер операции: '))
            print('\n')

            if num_operation == 1:
                for item in db.get_companies_and_vacancies_count():
                    print(item)
            elif num_operation == 2:
                for item in db.get_all_vacancies():
                    print(item)
            elif num_operation == 3:
                print(f"Средняя зарплата по всем вакансиям {db.get_avg_salary()} руб.")
            elif num_operation == 4:
                for item in db.get_vacancies_with_higher_salary():
                    print(item)
            elif num_operation == 5:
                search_word = input("Введи слово для поиска по вакансиям: ")
                result = db.get_vacancies_with_keyword(search_word)
                for item in result:
                    print(item)
            elif num_operation == 0:
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте еще раз!")
                continue


def get_vacancies_write_db() -> None:
    params = config()
    db = DBWrite('hh_ru', params)

    list_employers = LIST_EMPLOYERS
    count_vacancies = 0
    for employer in list_employers:
        count_vacancies += len(get_vacancies_by_employer(employer))
        db.write_db(get_employer_info(employer), get_vacancies_by_employer(employer))

    print(f"\nБД обновлена\n{count_vacancies} вакансий найдено.")


if __name__ == '__main__':
    print("Добро пожаловать!!!")

    while True:
        print("\nГлавное меню\n"
              "  1 - Обновить БД вакансий\n"
              "  2 - Подключиться к БД вакансий\n"
              "  0 - Выход")
        input_operation = input(" ->: ")

        if input_operation == '1':
            print("Подождите, идет поиск вакансий...\n")
            get_vacancies_write_db()
        elif input_operation == '2':
            user_interface()
        else:
            exit()
