import elements

from dash import Dash, html, dcc


class Server:
    def __init__(self, app: Dash):
        self.app = app
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = html.Div(
            children=[
                html.Div(
                    children=[html.H1("REPRESENTATIVES OF THE IX-th SEJM CADENCY")],
                    className="title-section",
                ),
                html.Br(),
                elements.get_sejm_plot_section(),
                html.Br(),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H1("Political Parties"),
                                html.H2("Prawo i Sprawiedliwość"),
                                html.Img(src="\\assets\\Logo_PiS.svg.png", alt="PiS"),
                                html.Br(),
                                html.H2("Koalicja Obywatelska"),
                                html.Img(src="\\assets\\Logo_KO.png", alt="KO"),
                                html.Br(),
                                html.H2("Lewica"),
                                html.Img(src="\\assets\\Logo_Lewica.png", alt="Lewica"),
                                html.Br(),
                                html.H2("Koalicja Polska"),
                                html.Img(src="\\assets\\Logo_PSL.png", alt="KP"),
                                html.Br(),
                                html.H2("Konfederacja"),
                                html.Img(
                                    src="\\assets\\Logo_Konfederacja.png",
                                    alt="Konfederacja",
                                ),
                                html.Br(),
                                html.H2("Polska2050"),
                                html.Img(src="\\assets\\Logo_2050.png", alt="2050"),
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
            ]
        )

    def run(self):
        self.app.run_server(debug=True)
