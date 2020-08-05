from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
)


def cb_echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.effective_user.id
    )


def cb_caps(update, context):
    text_caps = ' '.join(context.args).upper()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
    )


handlers = [
    CommandHandler('caps', cb_caps),
    MessageHandler(Filters.text & (~Filters.command), cb_echo),
]
