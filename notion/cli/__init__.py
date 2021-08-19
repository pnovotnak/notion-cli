import logging
import os
from pathlib import Path

import yaml
import click as click

from ..todo import TodoClient, Todo
from ..types import FILTERS, SORTS


@click.group()
@click.option('--config', default=Path(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'))
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, config, debug):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    with open(config) as fp:
        config = yaml.load(fp, Loader=yaml.SafeLoader)

    ctx.obj = TodoClient(**config['client'], **config['todos'])


@cli.command()
@click.pass_context
def get_todos(ctx, category: str, complete: bool = False):
    client = ctx.obj
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
    results = client.query_database(client.db, query=query, sorts=[
        SORTS['due'](),
        SORTS['created']()
    ])['results']

    out = []
    for result in results:
        out.append(Todo(result))
    return out


def print_todos(ctx, *args, **kwargs):
    for todo in ctx.obj.get_todos(*args, **kwargs):
        print(todo)


def create_todo(ctx, title, category):
    """ Create a to-do in the database
    See: https://developers.notion.com/reference/post-page
    """
    ctx.obj.post('pages', json={
        'parent': {
            'type': 'database_id',
            'database_id': ctx.db
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


def archive_todo(ctx, page_id):
    ctx.obj.patch(f'pages/{page_id}', json={"archived": True})
