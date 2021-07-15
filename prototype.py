#!/bin/sh
"true" '''\'
exec "$(dirname "$(readlink "$0")")"/venv/bin/python "$0" "$@"
'''

__doc__ = """You will need to deliberately set your docstrings though"""

import argparse
import sys

import yaml

from todo import TodoClient


if __name__ == "__main__":
    with open('config.yaml') as fp:
        config = yaml.load(fp, Loader=yaml.SafeLoader)
    client = TodoClient(**config['client'], **config['todos'])

    parser = argparse.ArgumentParser(description='Notion Todos from the CLI')
    subparsers = parser.add_subparsers()

    parser_get_todos = subparsers.add_parser('get-todos', help='list top 20 by app')
    parser_get_todos.set_defaults(func=client.print_todos)
    parser_get_todos.add_argument('category', type=str, choices=['work', 'life'], help='Which category of todos to show')
    parser_get_todos.add_argument('--complete', type=bool, default=False, help='Show completed todos')

    parser_get_todos = subparsers.add_parser('create-todo', help='create a todo')
    parser_get_todos.set_defaults(func=client.create_todo)
    parser_get_todos.add_argument('category', type=str, choices=['work', 'life'], help='Which category of todos to show')
    parser_get_todos.add_argument('title', type=str, help='Title of the todo')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    args = parser.parse_args().__dict__
    func = args['func']
    del args['func']
    func(**args)
