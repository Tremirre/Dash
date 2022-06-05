import elements

import dash_bootstrap_components as dbc
from dash import html, dcc

PAGE_1 = [
    elements.get_nav_bar(),
    *elements.get_hidden_panel_elements(),
    elements.get_sejm_plot_section(),
    elements.get_repr_vis_section(),
]

PAGE_2 = [
    elements.get_nav_bar(),
    elements.get_party_plot_section(),
    elements.get_party_stats_section(),
]

PAGE_3 = [
    elements.get_nav_bar(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(children=[
        html.H1("Select feature to analyse"),
        dcc.Dropdown(
            id="dropdown-2",
            options=[
                "education",
                "occupation",
                "vehicles_count",
                "cash_polish_currency",
                "cash_foreign_currency",
                "paper_value",
                "loans_value",
                'total_funds',
                'num_houses',
                'num_flats',

            ],
            value="education",
            multi=False
        ),
        dcc.Graph(config={"displayModeBar": False, "autosizable": True, "responsive": True}, id="bar-plot"),
        dbc.Container(id = "table"),
    ]),
    html.P(id="placeholder"),
]
