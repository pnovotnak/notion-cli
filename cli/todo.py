from typing import List

from colors import color

from notion.client import NotionClient
from notion.types import DueDate, FILTERS, SORTS


def xterm_link(text, url):
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'


class Todo:
    id = None
    url = None
    title = None
    due = None

    def __init__(self, raw):
        properties = raw['properties']
        self.id = raw['id']
        self.url = raw["url"]
        self.title = properties["Text"]["title"][0]["text"]["content"]

        try:
            self.due = DueDate(properties["Due"])
        except KeyError:
            self.due = None

    def __str__(self):
        line = [
            self.title,
        ]

        color_args = {}
        if self.due and self.due.is_due():
            color_args = {'fg': 'red'}

        # rendered_li = f'{self.id}\t{" ".join(line)}'
        rendered_li = f'- {" ".join(line)}'
        return color(f'{xterm_link(rendered_li, self.url)}', **color_args)


class TodoClient(NotionClient):
    db = None

    def __init__(self, bearer_token, db):
        super().__init__(bearer_token)
        self.db = db

    def get_todos(self, category: str, complete: bool = False):
        query = {
            "or": [
                {
                    "and": [
                        FILTERS['type'](category),
                        FILTERS['complete'](complete)
                    ]
                },
                {
                    "and": [
                        FILTERS['type'](None),
                        FILTERS['complete'](complete)
                    ]
                }
            ]
        }
        results = self.query_database(self.db, query=query, sorts=[
            SORTS['due'](),
            SORTS['created']()
        ])['results']

        out = []
        for result in results:
            out.append(Todo(result))
        return out

    def print_todos(self, *args, **kwargs):
        for todo in self.get_todos(*args, **kwargs):
            print(todo)

    def create_todo(self, title, category):
        """ Create a to-do in the database
        See: https://developers.notion.com/reference/post-page
        """
        self.post('pages', json={
            'parent': {
                'type': 'database_id',
                'database_id': self.db
            },
            'archived': False,
            'properties': {
                # 'Meeting': {'type': 'relation', 'relation': []},
                # 'Due': {'type': 'date', 'date': {'start': '2021-06-17', 'end': None}},
                # 'Done': {'type': 'checkbox', 'checkbox': False},
                # 'Project': {'relation': [{'id': 'fdd80593-7034-49b3-a138-ab8b39450fca'}]},
                'Type': {
                    'type': 'select',
                    'select': {
                        'name': category
                    }
                },
                'Text': {
                    'title': [
                        {
                            'text': {
                                'content': title,
                            },
                        }
                    ]
                }
            },
        })

    def archive_todo(self, page_id):
        self.patch(f'pages/{page_id}', json={"archived": True})
