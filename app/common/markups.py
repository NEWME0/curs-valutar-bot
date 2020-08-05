from typing import List

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from app.common.models import (
    BankItem,
    CoinItem,
)


def markup_select_bank(bank_list: List[BankItem]) -> ReplyKeyboardMarkup:
    column = list()
    for item in bank_list:
        button = KeyboardButton(text=item.registered_name)
        column.append([button])
    markup = ReplyKeyboardMarkup(column)
    return markup


def markup_select_coin(coin_list: List[CoinItem]) -> ReplyKeyboardMarkup:
    count_per_row = 5
    keyboard = list()
    for i in range(0, len(coin_list), count_per_row):
        row = list()
        for coin in coin_list[i:i+count_per_row]:
            row.append(
                KeyboardButton(text=coin.abbr)
            )
        keyboard.append(row)
    markup = ReplyKeyboardMarkup(keyboard)
    return markup


def markup_coins(coins: List[str]) -> ReplyKeyboardMarkup:
    count_per_row = 5
    keyboard = list()
    for i in range(0, len(coins), count_per_row):
        row = list()
        for coin in coins[i:i+count_per_row]:
            row.append(
                KeyboardButton(text=coin)
            )
        keyboard.append(row)
    markup = ReplyKeyboardMarkup(keyboard)
    return markup
