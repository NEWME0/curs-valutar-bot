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
    reply_internal_error,
    reply_cancel_info,
    reply_cancel_text,
    reply_select_coin,
    reply_unknown_coin,
)

from app.common.markups import (
    markup_coins,
)

import app.services.curs_valutar_api as api


COIN = 0
END = ConversationHandler.END,


def cb_best_buy(update, context):
    coins = api.request_coins_all()
    if not coins:
        reply_internal_error(update, context, ReplyKeyboardRemove())
        return END

    coins_abbr = list(set(coin.abbr for coin in coins))
    markup = markup_coins(coins_abbr)

    reply_select_coin(update, context, markup)
    reply_cancel_info(update, context)

    return COIN


def cb_best_buy_coins(update, context):
    coins = api.request_coins_with_abbr(update.message.text)
    if not coins:
        reply_unknown_coin(update, context)
        reply_cancel_info(update, context)
        return COIN

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

        data.append(
            [rate.date, rate.rate_buy, bank.registered_name]
        )

    update.message.reply_text(str(data))
    reply_cancel_info(update, context)

    return COIN


def cb_cancel(update: Update, context):
    reply_cancel_text(update, context, ReplyKeyboardRemove())
    return END


best_buy = ConversationHandler(
    entry_points=[
        CommandHandler('best_buy', cb_best_buy),
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
    best_buy,
]
