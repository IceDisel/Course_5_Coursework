from configparser import ConfigParser


def config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """
    Функция чтения конфигурационного файла .ini
    :param filename: Имя файла
    :param section: Чтение секции файла
    :return: Словарь с параметрами
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
