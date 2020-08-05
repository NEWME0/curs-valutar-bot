from telegram.ext import (
    CommandHandler,
)

from app.common.replies import (
    reply_start,
    reply_help,
)


def cb_start(update, context):
    reply_start(update, context)
    reply_help(update, context)


def cb_help(update, context):
    reply_help(update, context)


handlers = [
    CommandHandler('start', cb_start),
    CommandHandler('help', cb_help),
]
