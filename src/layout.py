import elements

from dash import html, dcc

PAGE_1 = [
    elements.get_nav_bar(),
    elements.get_sejm_plot_section(),
    elements.get_repr_vis_section(),
]

PAGE_2 = [
    elements.get_nav_bar(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(children=[html.H1("PAGE 2....")]),
    html.H1("BBBBBBBBBBBBBBBBBBB"),
]

PAGE_3 = [
    elements.get_nav_bar(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1("Political Parties"),
                    html.H2("Prawo i Sprawiedliwość"),
                    html.Img(src="assets/logos/Logo_PiS.svg.png", alt="PiS"),
                    html.Br(),
                    html.H2("Koalicja Obywatelska"),
                    html.Img(src="assets/logos/Logo_KO.png", alt="KO"),
                    html.Br(),
                    html.H2("Lewica"),
                    html.Img(src="assets/logos/Logo_Lewica.png", alt="Lewica"),
                    html.Br(),
                    html.H2("Koalicja Polska"),
                    html.Img(src="assets/logos/Logo_PSL.png", alt="KP"),
                    html.Br(),
                    html.H2("Konfederacja"),
                    html.Img(
                        src="assets/logos/Logo_Konfederacja.png",
                        alt="Konfederacja",
                    ),
                    html.Br(),
                    html.H2("Polska2050"),
                    html.Img(src="assets/logos/Logo_2050.png", alt="2050"),
                ],
                className="logo",
            )
        ],
        className="partie",
    ),
    html.Br(),
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
