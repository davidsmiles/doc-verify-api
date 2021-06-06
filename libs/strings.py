"""
libs.strings
By default, uses 'en-gb.json' file inside 'strings' top-level folder
If language changes, set 'libs.strings.default_locale' and run 'libs.strings.refresh()'
"""

import json

default_locale = 'en-us'
cached_strings = {}


def refresh():
    with open(f'strings/{default_locale}.json') as file:
        global cached_strings
        cached_strings = json.load(file)


def gettext(name: str):
    return cached_strings[name]


def get_all():
    return cached_strings


def set_default_locale(locale):
    global default_locale
    default_locale = locale
    refresh()


def set_api_spec(locale):
    global default_locale
    default_locale = locale
    refresh()


refresh()