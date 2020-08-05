import logging
import itertools
from telegram.ext import Updater

from app.config import (
    CURS_VALUTAR_BOT_TOKEN,
    CURS_VALUTAR_BOT_WEBHOOK_HOST,
    CURS_VALUTAR_BOT_WEBHOOK_PORT,
    CURS_VALUTAR_BOT_WEBHOOK_PATH,
    CURS_VALUTAR_BOT_WEBHOOK_URL
)

from app.handlers import (
    debug,
    evolution,
    actual,
    best,
    default,
    feature,
    unknown,
)

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
    level=logging.DEBUG
)


# Init bot updater
updater = Updater(
    token=CURS_VALUTAR_BOT_TOKEN,
    use_context=True
)


# Set handlers here...
for handler in itertools.chain(
    default.handlers,
    evolution.handlers,
    actual.handlers,
    best.handlers,
    unknown.handlers,
):
    updater.dispatcher.add_handler(handler)


# Set webhook and start listening
updater.start_webhook(
    listen=CURS_VALUTAR_BOT_WEBHOOK_HOST,
    port=CURS_VALUTAR_BOT_WEBHOOK_PORT,
    url_path=CURS_VALUTAR_BOT_WEBHOOK_PATH,
)

# Send webhook url to Telegram server
updater.bot.set_webhook(
    url=CURS_VALUTAR_BOT_WEBHOOK_URL,
)

# Stop on KeyboardInterrupt [CTRL+C]
updater.idle()
