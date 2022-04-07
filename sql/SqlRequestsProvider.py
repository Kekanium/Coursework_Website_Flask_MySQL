import os
from string import Template


class SqlRequestsProvider:
    """
    Class for creation SQL requests
    """

    def __init__(self, filePath):
        """

        :param filePath: Path to SQL requests folder
        """
        self._scripts = {}

        for file in os.listdir(filePath):
            _, expression = os.path.splitext(file)
            if expression == '.sql':
                self._scripts[file] = Template(open(f'{filePath}/{file}', 'r').read())

    def getRequest(self, fileName, **kwargs):
        """
        Create SQL requests, using substitute to parametrize request

        :param fileName: Name of the request
        :param kwargs: Request params
        :return: Parametrized request
        """
        return self._scripts[fileName].substitute(**kwargs)
