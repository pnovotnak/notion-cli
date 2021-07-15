import datetime

import requests


FILTERS = {
    'type': lambda t: {
        "property": "Type",
        "select": {
            "equals": t,
        }
    },
    'complete': lambda complete=False: {
        "property": "Done",
        "checkbox": {
            "equals": complete,
        }
    }
}

SORTS = {
    'created': lambda direction='ascending': {
        "property": "Created",
        "direction": direction,
    },
    'due': lambda direction='descending': {
        "property": "Due",
        "direction": direction,
    }
}


class NotionClient(requests.Session):
    headers = dict()

    def __init__(self, bearer_token, root_url='https://api.notion.com/v1'):
        self.root_url = root_url
        super(NotionClient, self).__init__()
        self.headers.update({
            'Authorization': f'Bearer {bearer_token}',
            'Notion-Version': '2021-05-13',
        })

    def search(self, query: str, sort: dict = None):
        """ Search for things within notion. We'll only have access to things which you have shared.
        Example:

        >>> dbs = notion.search('Todos')
        >>> dbs['results']

        :param query:
        :param sort:
        :return:
        """
        return self.post('search', {"query": query, "sort": sort}).json()

    def get_database(self, database_id):
        return self.get(f'databases/{database_id}').json()

    def query_database(self, database_id, query=None, sorts=None):
        q = self.post(f'databases/{database_id}/query', json={"filter": query, "sorts": sorts})
        return q.json()

    def request(self, method, path, **kwargs):
        return super(NotionClient, self).request(method, f'{self.root_url}/{path}', **kwargs)


class DateProperty:
    start = None
    end = None

    def __init__(self, property_data):
        for k, v in property_data['date'].items():
            if v:
                setattr(self, k, datetime.date.fromisoformat(v))


class TextPropterty:
    def __init__(self):
        pass


class DueDate(DateProperty):
    def is_due(self):
        return self.start <= datetime.date.today()
