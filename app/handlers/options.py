from datetime import date

from telegram import (
    Update,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    Filters,
)

from app.common.replies import (
    reply_typing,
    reply_internal_error,
    reply_cancel_info,
    reply_cancel_text,
    reply_select_coin,
    reply_unknown_coin,
)

from app.common.markups import markup_columns

import app.services.curs_valutar_api as api
from app.services.render_table import render_table_options


COIN = 0
END = ConversationHandler.END,


def cb_options(update, context):
    reply_typing(update, context)

    coins = api.request_coins_all()
    if not coins:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    markup = markup_columns(list(set(coin.abbr for coin in coins)), columns=5)
    reply_select_coin(update, context, markup)
    reply_cancel_info(update, context)
    return COIN


def cb_best_buy_coins(update, context):
    reply_typing(update, context)

    coins = api.request_coins_with_abbr(update.message.text)
    if not coins:
        reply_unknown_coin(update, context)
        reply_cancel_info(update, context)
        return COIN

    selected_coin_abbr = update.message.text

    rates = api.request_rates_of_coins([coin.id for coin in coins])
    if not rates:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    banks = api.request_banks_with_ids([coin.bank for coin in coins])
    if not banks:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    data = list()
    for rate in rates:
        coin = next(coin for coin in coins if coin.id == rate.currency)
        bank = next(bank for bank in banks if bank.id == coin.bank)
        data.append([rate.date, coin.abbr, rate.rate_buy, rate.rate_sell, bank.registered_name])

    # Transpose table
    data = list(map(list, zip(*data)))

    table_path = render_table_options(
        cells=data,
        coin_abbr=selected_coin_abbr,
        actual_date=date.today(),
    )

    update.message.reply_photo(photo=open(table_path, 'rb'))
    reply_cancel_info(update, context)

    return COIN


def cb_cancel(update: Update, context):
    reply_typing(update, context)
    reply_cancel_text(update, context, ReplyKeyboardRemove())
    return END


options = ConversationHandler(
    entry_points=[
        CommandHandler('options', cb_options),
    ],
    states={
        COIN: [
            CommandHandler('cancel', cb_cancel),
            MessageHandler(Filters.text, cb_best_buy_coins),
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cb_cancel),
    ]
)

handlers = [
    options,
]
