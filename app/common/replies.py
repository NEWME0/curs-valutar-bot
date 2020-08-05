

def reply_start(update, context, markup=None):
    update.message.reply_text(
        "Curl Valutar Bot - https://www.live.curs-valutar.xyz/"
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry \n"
        "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\n"
        "when an unknown printer took a galley of type and scrambled it to make\n",
        reply_markup=markup,
    )


def reply_help(update, context, markup=None):
    update.message.reply_text(
        'Lista de comenzi disponibile:\n'  # noqa
        '/start - initierea dialogului\n'  # noqa
        '/help - lista de commenzi disponibile\n'  # noqa
        '/evolution - evolutia valutei pentru ultimile 7 zile\n'  # noqa
        '/actual - ratele de schimb actuale\n'  # noqa
        '/best_sell - cea mai buna optiune de vinzare\n'  # noqa
        '/best_buy - cea mai buna optiune de cumparare\n',  # noqa
        reply_markup=markup,
    )


def reply_help_info(update, context, markup=None):
    update.message.reply_text(
        '/help - lista de comenzi disponibile\n',  # noqa
        reply_markup=markup,
    )


def reply_internal_error(update, context, markup=None):
    update.message.reply_text(
        'Din pacate a avut loc erroare tehnica\n'  # noqa
        'Incercati din nou mai tirziu\n',  # noqa
        reply_markup=markup,
    )


def reply_select_bank(update, context, markup=None):
    update.message.reply_text(
        'Alege una din bancile din lista\n',  # noqa
        reply_markup=markup,
    )


def reply_select_coin(update, context, markup=None):
    update.message.reply_text(
        'Alege una din valutele din lista\n',  # noqa
        reply_markup=markup,
    )


def reply_unknown_bank(update, context, markup=None):
    update.message.reply_text(
        'Banca introdusa nu face parte din lista\n',  # noqa
        reply_markup=markup,
    )


def reply_unknown_coin(update, context, markup=None):
    update.message.reply_text(
        'Valuta introdusa nu face parte din lista\n',  # noqa
        reply_markup=markup,
    )


def reply_cancel_info(update, context, markup=None):
    update.message.reply_text(
        '/cancel - iesire din conversatie\n',  # noqa
        reply_markup=markup,
    )


def reply_cancel_text(update, context, markup=None):
    update.message.reply_text(
        '/help - lista de comenzi disponibile\n',  # noqa
        reply_markup=markup,
    )


def reply_unknown_message(update, context, markup=None):
    update.message.reply_text(
        'Din pacate nu inteleg ce vreti sa spuneti\n',  # noqa
        reply_markup=markup,
    )


def reply_unknown_command(update, context, markup=None):
    update.message.reply_text(
        'Din pacate nu inteleg aceasta comanda\n',  # noqa
        reply_markup=markup,
    )
