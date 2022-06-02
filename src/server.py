import elements

from dash import Dash, html, dcc

import layout


class Server:
    def __init__(self, app: Dash):
        self.app = app
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = html.Div(id="page-layout", children=layout.PAGE_1)

    def run(self):
        self.app.run_server(debug=True)
