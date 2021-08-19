from colors import color

from notion.client import NotionClient
from notion.types import DueDate


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
