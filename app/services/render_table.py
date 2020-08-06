import os
from datetime import date
from typing import List
from plotly.graph_objects import Figure, Table
from plotly.colors import qualitative

from app.config import IMAGES_ROOT


def render_table(cells: List[List], header: List[str], title: str) -> Figure:
    header_dict = dict(
        values=header,
        line_color='white',
        fill_color=qualitative.T10[2],
        align='left',
        font=dict(
            color='white',
            family="Lato",
            size=20,
        ),
        height=30,
    )

    cells_dict = dict(
        values=cells,
        line_color='white',
        fill_color=qualitative.G10[9],
        align='left',
        font=dict(
            color='white',
            family="Lato",
            size=20,
        ),
        height=30,
    )

    table = Table(
        header=header_dict,
        cells=cells_dict,
    )

    figure = Figure(
        data=[table],
    )

    figure.update_layout(
        margin=dict(l=20, r=20, t=100, b=20),
        paper_bgcolor=qualitative.G10[9],
        font_family="Late",
        font_color="white",
        title_text=title,
        title_x=0.5,
        title_font_family="Late",
        title_font_color="white",
        title_font_size=30,
    )

    return figure


def render_table_options(cells: List[List], coin_abbr: str, actual_date: date) -> str:
    title = f'{coin_abbr} - {actual_date}'
    header = ['Data', 'Valuta', 'Vinzare', 'Cumparare', 'Banca']  # noqa

    image_name = f'table_rates_options_{coin_abbr}_{actual_date}.png'
    image_path = os.path.join(IMAGES_ROOT, image_name)

    # TODO: Check if image already exists

    figure = render_table(cells, header, title)
    figure.write_image(image_path)

    return image_path


def render_table_actual(cells: List[List], bank_name: str, actual_date: date) -> str:
    title = f'{bank_name} - {actual_date}'
    header = ['Data', 'Valuta', 'Vinzare', 'Cumparare']  # noqa

    image_name = f'table_rates_actual_{bank_name}_{actual_date}.png'
    image_path = os.path.join(IMAGES_ROOT, image_name)

    # TODO: Check if image already exists

    figure = render_table(cells, header, title)
    figure.write_image(image_path)

    return image_path
