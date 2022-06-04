import elements

import dash_bootstrap_components as dbc
from dash import html, dcc

PAGE_1 = [
    elements.get_nav_bar(),
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
    html.Div(children=[
        html.H4("Analysis of parties"),
        dcc.Dropdown(
            id="dropdown-2",
            options=[
                "education",
                "occupation",
                "vehicles_count",
                "cash_polish_currency",
                "cash_foreign_currency",
                "paper_value",
                "loans_value"

            ],
            value="education",
            multi=False
        ),
        dcc.Graph(id="bar-plot"),
        dbc.Container(id = "table"),
    ]),
    html.Div(
        [
            html.H4("Analysis of hajsik data using scatter matrix"),
            dcc.Dropdown(
                id="dropdown",
                options=[
                    "cash_polish_currency",
                    "cash_foreign_currency",
                    "paper_value",
                    "property_value",
                    "vehicles_count",
                ],
                value=["cash_polish_currency", "cash_foreign_currency"],
                multi=True,
            ),
            dcc.Graph(id="scatter_matrix"),
        ]
    ),
    html.P(id="placeholder"),
]

