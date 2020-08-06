from datetime import date

from telegram import (
    Update,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Filters,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)

from app.common.replies import (
    reply_typing,
    reply_internal_error,
    reply_select_bank,
    reply_unknown_bank,
    reply_cancel_info,
    reply_cancel_text,
)

from app.common.markups import markup_columns

import app.services.curs_valutar_api as api
from app.services.render_table import render_table_actual


BANK = 0
END = ConversationHandler.END


def cb_actual(update: Update, context: CallbackContext):
    reply_typing(update, context)

    banks = api.request_banks_all()
    if not banks:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    markup = markup_columns([bank.registered_name for bank in banks], columns=1)
    reply_select_bank(update, context, markup)
    reply_cancel_info(update, context)

    context.user_data['banks'] = banks

    return BANK


def cb_bank(update: Update, context: CallbackContext):
    reply_typing(update, context)

    selected_bank = next((b for b in context.user_data['banks'] if b.registered_name == update.message.text), None)
    if not selected_bank:
        reply_unknown_bank(update, context)
        reply_cancel_info(update, context)
        return BANK

    coins = api.request_coins_of_bank(selected_bank.id)
    if not coins:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    rates = api.request_rates_of_coins([coin.id for coin in coins])
    if not rates:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    data = list()
    for rate in rates:
        coin = next(coin for coin in coins if coin.id == rate.currency)
        data.append([rate.date, coin.abbr, rate.rate_sell, rate.rate_buy])

    # Transpose table
    data = list(map(list, zip(*data)))

    table_path = render_table_actual(
        cells=data,
        bank_name=selected_bank.registered_name,
        actual_date=date.today(),
    )

    update.message.reply_photo(photo=open(table_path, 'rb'))
    reply_cancel_info(update, context)

    return BANK


def cb_cancel(update: Update, context: CallbackContext):
    reply_typing(update, context)
    reply_cancel_text(update, context, ReplyKeyboardRemove())
    return ConversationHandler.END


rates_actual = ConversationHandler(
    entry_points=[
        CommandHandler('actual', cb_actual),
    ],
    states={
        BANK: [
            CommandHandler('cancel', cb_cancel),
            MessageHandler(Filters.text, cb_bank),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cb_cancel),
    ]
)

handlers = [
    rates_actual,
]
