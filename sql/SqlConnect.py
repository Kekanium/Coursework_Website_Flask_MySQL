from pymysql import connect
from pymysql.err import OperationalError


class SqlConnect:
    """
    Class to create connection to SQL database
    """
    def __init__(self, config: dict):
        """
        Constructor for SqlConnect

        :param config: config for SQL database
        """
        self.config = config
        self.cursor = None
        self.conn = None
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Неверный логин и пароль, повторите подключение')
            if err.args[0] == 2003:
                print('Неверно введен порт или хост для подключения к серверу')
            if err.args[0] == 1049:
                print('Такой базы данных не существует')
        except UnicodeEncodeError:
            print('Были введены символы на русском языке')

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value:
            if exc_value.args[0] == 'Cursor is None':
                print('Курсор не создан')
            elif exc_value.args[0] == 1064:
                print('Синтаксическая ошибка в запросе!')
            elif exc_value.args[0] == 1146:
                print('Ошибка в запросе! Такой таблицы не существует.')
            elif exc_value.args[0] == 1054:
                print('Ошибка в запросе! Такого поля не существует.')
        if self.conn is not None and self.cursor is not None:
            self.conn.commit()
            self.conn.close()
        return True
