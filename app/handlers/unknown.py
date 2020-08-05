from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from telegram.ext import (
    Filters,
    MessageHandler,
)

from app.common.replies import (
    reply_help_info,
    reply_unknown_message,
    reply_unknown_command,
)


def cb_unknown_message(update: Update, context: CallbackContext):
    reply_unknown_message(update, context)
    reply_help_info(update, context)


def cb_unknown_command(update: Update, context: CallbackContext):
    reply_unknown_command(update, context)
    reply_help_info(update, context)


handlers = [
    MessageHandler(Filters.text, cb_unknown_message),
    MessageHandler(Filters.command, cb_unknown_command),
]
