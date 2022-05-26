import elements

from dash import Dash, html, dcc

class Server:
    def __init__(self, app: Dash):
        self.app = app
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = html.Div(
            children=[
                html.H1(children=["TESTING DASH APP"]),
                dcc.Input(id="test_input", value="", type="text"),
                html.Br(),
                html.Div(id="test_output"),
                html.Br(),
                html.Div(
                    children=[
                        elements.get_main_sejm_plot(),
                        html.Div(
                            children=[
                                html.H1("CONTAINED"),
                                html.Br(),
                                html.H3("Some dumb text as a placeholder to this beatutiful beautiful dashboard that greatly rerpesents my programming skills and sense of beauty."),
                                html.Pre(id="debug-output")
                            ],
                            className="side-bar"
                        )
                    ],
                    className="sejm-plot-section"
                )
            ]
        )

    def run(self):
        self.app.run_server(debug=True)