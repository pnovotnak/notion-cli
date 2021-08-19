import requests


class NotionClient(requests.Session):
    headers = dict()

    def __init__(self, bearer_token, root_url='https://api.notion.com/v1'):
        self.root_url = root_url
        super(NotionClient, self).__init__()
        self.headers.update({
            'Authorization': f'Bearer {bearer_token}',
            'Notion-Version': '2021-05-13',
        })

    def search(self, query: str, **kwargs):
        """ Search for things within notion. We'll only have access to things which you have shared.
        Example:

        >>> dbs = notion.search('Todos')
        >>> dbs['results']

        :param query:
        :param sort:
        :return:
        """
        body = {"query": query}
        body.update(kwargs)
        return self.post('search', body).json()

    def get_database(self, database_id):
        return self.get(f'databases/{database_id}').json()

    def query_database(self, database_id, query=None, sorts=None):
        q = self.post(f'databases/{database_id}/query', json={"filter": query, "sorts": sorts})
        return q.json()

    def request(self, method, path, **kwargs):
        return super(NotionClient, self).request(method, f'{self.root_url}/{path}', **kwargs)
