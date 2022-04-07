import pymysql

from sql.SqlConnect import SqlConnect
from sql.SqlRequestsProvider import SqlRequestsProvider


class SqlMaster:
    """
    Master class to interact with SQL database
    """

    def __init__(self, dataBaseConfig: dict, requestsPath: str):
        """
        :param dataBaseConfig: config for SQL database
        :param requestsPath: Path to SQL requests
        """
        self.dataBaseConnect = SqlConnect(dataBaseConfig)
        self.dataBaseRequest = SqlRequestsProvider(requestsPath)

    def MakeRequest(self, filename: str, **kwargs) -> list:
        """
        Make request to specified SQL database

        :param filename: Name of the request
        :param kwargs: Request params
        :return: result of SQL request in format list of dicts
        """
        cursor = self.dataBaseConnect.cursor
        request = self.dataBaseRequest.getRequest(filename, **kwargs)
        if cursor is None:
            raise ValueError('Cursor is None')
        elif cursor:
            cursorDict = self.dataBaseConnect.conn.cursor(pymysql.cursors.DictCursor)
            cursorDict.execute(request)
            result = cursorDict.fetchall()
            self.dataBaseConnect.conn.commit()
            return result

    def MakeUpdateInsert(self, filename: str, **kwargs) -> None:
        """
        Make update/request/delete to specified SQL database

        :param filename: Name of the request
        :param kwargs: Request params
        :return: result of SQL request in format list of dicts
        """
        cursor = self.dataBaseConnect.cursor
        request = self.dataBaseRequest.getRequest(filename, **kwargs)
        if cursor is None:
            raise ValueError('Cursor is None')
        elif cursor:
            cursor.execute(request)
            self.dataBaseConnect.conn.commit()
            return None
