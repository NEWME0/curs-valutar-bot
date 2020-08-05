from datetime import date, timedelta

from telegram import (
    Update,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
)

from app.common.replies import (
    reply_internal_error,
    reply_select_bank,
    reply_select_coin,
    reply_unknown_bank,
    reply_unknown_coin,
    reply_cancel_info,
    reply_cancel_text,
)

from app.common.markups import (
    markup_select_bank,
    markup_select_coin,
)

import app.services.curs_valutar_api as api
from app.services.plot_renderer import plot_rates_evolution


BANK, COIN = range(2)
END = ConversationHandler.END


def cb_evolution(update: Update, context: CallbackContext):
    banks = api.request_banks_all()
    if not banks:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    context.user_data['banks'] = banks

    markup = markup_select_bank(banks)
    reply_select_bank(update, context, markup)
    reply_cancel_info(update, context)

    return BANK


def cb_bank(update: Update, context: CallbackContext):
    for selected_bank in context.user_data['banks']:
        if update.message.text == selected_bank.registered_name:
            break
    else:
        reply_unknown_bank(update, context)
        reply_cancel_info(update, context)
        return BANK

    context.user_data['selected_bank'] = selected_bank

    coins = api.request_coins_of_bank(selected_bank.id)
    if not coins:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    context.user_data['coins'] = coins

    markup = markup_select_coin(coins)
    reply_select_coin(update, context, markup)
    reply_cancel_info(update, context)

    return COIN


def cb_coin(update: Update, context: CallbackContext):
    for selected_coin in context.user_data['coins']:
        if update.message.text == selected_coin.abbr:
            break
    else:
        reply_unknown_coin(update, context)
        reply_cancel_info(update, context)
        return COIN

    rates = api.request_rates_of_coin(selected_coin.id, date.today() - timedelta(days=7))
    if not rates:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    png_path = plot_rates_evolution(
        rate_list=rates,
        bank_name=context.user_data['selected_bank'].registered_name,
        coin_name=selected_coin.abbr,
    )

    update.message.reply_photo(
        photo=open(png_path, 'rb'),
    )
    reply_select_coin(update, context)
    reply_cancel_info(update, context)

    return COIN


def cb_cancel(update: Update, context: CallbackContext):
    reply_cancel_text(update, context, ReplyKeyboardRemove())
    return ConversationHandler.END


coin_evolution = ConversationHandler(
    entry_points=[
        CommandHandler('evolution', cb_evolution),
    ],
    states={
        BANK: [
            CommandHandler('cancel', cb_cancel),
            MessageHandler(Filters.text, cb_bank),
        ],
        COIN: [
            CommandHandler('cancel', cb_cancel),
            MessageHandler(Filters.text, cb_coin),
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cb_cancel),
    ]
)


handlers = [
    coin_evolution,
]
