from typing import List, Iterable

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def group_by(it: Iterable, by: int = 1):
    """ group_by(it=[1, 2, 3, 4, 5, 6], by=2) -> [[1, 2], [3, 4], [5, 6]] """
    result = list()
    for i in range(0, len(it), by):
        result.append(it[i:i+by])
    return result


def markup_columns(keys: List[str], columns: int = 2) -> ReplyKeyboardMarkup:
    """ Make keyboard markup with specified number of columns """
    buttons = [KeyboardButton(text=key) for key in keys]
    keyboard = group_by(buttons, columns)
    markup = ReplyKeyboardMarkup(keyboard)
    return markup


def markup_remove():
    return ReplyKeyboardRemove()
