#!/bin/sh
"true" '''\'
exec "$(dirname "$(readlink "$0")")"/venv/bin/python "$0" "$@"
'''

# This file can be executed by either sh or python
__doc__ = """Notion CLI"""

from notion.cli import cli

if __name__ == '__main__':
    cli(auto_envvar_prefix='NOTION_CLI')

"""

import argparse
import json
import sys
import os
from pathlib import Path

import yaml

from cli.todo import TodoClient


if __name__ == "__main__":
    with open(Path(os.path.dirname(os.path.realpath(__file__)), 'config.yaml')) as fp:
        config = yaml.load(fp, Loader=yaml.SafeLoader)
    client = TodoClient(**config['client'], **config['todos'])

    parser = argparse.ArgumentParser(description='Notion Todos from the CLI')
    subparsers = parser.add_subparsers()

    parser_get_todos = subparsers.add_parser('get-todos', help='list top 20 by app')
    parser_get_todos.set_defaults(func=client.print_todos)
    parser_get_todos.add_argument('category', type=str, choices=['work', 'life'], help='Which category of todos to show')
    parser_get_todos.add_argument('--complete', type=bool, default=False, help='Show completed todos')

    parser_create_todo = subparsers.add_parser('create-todo', help='create a todo')
    parser_create_todo.set_defaults(func=client.create_todo)
    parser_create_todo.add_argument('category', type=str, choices=['work', 'life'], help='Which category of todos to show')
    parser_create_todo.add_argument('title', type=str, help='Title of the todo')

    parser_delete_todo = subparsers.add_parser('delete-todo', help='delete (archive) a todo')
    parser_delete_todo.set_defaults(func=client.archive_todo)
    parser_delete_todo.add_argument('page_id', type=str, help='The ID of the todo')

    # The search API is somewhat... Lackluster. However, this _does_ work. The output is valid JSON and can be piped to
    # jq.
    parser_search = subparsers.add_parser('search', help='Search to perform')
    parser_search.set_defaults(func=lambda query: print(json.dumps(client.search(query)['results'])))
    parser_search.add_argument('query', type=str, help='Query')
    # TODO
    # parser_search.add_argument('filter', default=None, type=dict)

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    args = parser.parse_args().__dict__
    func = args['func']
    del args['func']
    func(**args)
"""
