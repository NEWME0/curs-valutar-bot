import os
from datetime import date
from typing import List
from plotly.graph_objects import Figure, Table
from plotly.colors import qualitative

from app.config import IMAGES_ROOT


def render_rates_actual(cells: List[List], bank_name: str, actual_date: date) -> str:
    image_name = f'table_rates_actual_{bank_name}_{actual_date}.png'
    image_path = os.path.join(IMAGES_ROOT, image_name)

    header = ['Data', 'Valuta', 'Vinzare', 'Cumparare']  # noqa

    header_dict = dict(
        values=header,
        line_color='white',
        fill_color=qualitative.T10[2],
        align='left',
        font=dict(
            color='white',
            family="Lato",
            size=30,
        ),
        height=40,
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
        title_text=f'{bank_name} - {actual_date}',  # noqa
        title_x=0.5,
        title_font_family="Late",
        title_font_color="white",
        title_font_size=30,
    )

    figure.write_image(image_path)

    return image_path
