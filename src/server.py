import dash_html_components as html
import dash_core_components as dcc

from dash import Dash

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
                html.Div(id="test_output")
            ]
        )

    def run(self):
        self.app.run_server(debug=True)