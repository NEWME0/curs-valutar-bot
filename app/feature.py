from datetime import date, timedelta
from app.services import curs_valutar_api as api

from app.services.render_table import render_rates_actual


cells = [
    [date.today(), 2, 3, 4],
    [date.today(), 2, 3, 4],
    [date.today(), 2, 3, 4],
    [date.today(), 2, 3, 4],
]


cells = list(map(list, zip(*cells)))


render_rates_actual(cells, 'bnm', date.today())
