import json

from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from elements import get_scatter_matrix

app = Dash(__name__)


@app.callback(
    Output(component_id="test_output", component_property="children"),
    Input(component_id="test_input", component_property="value"),
)
def update_test_output(value):
    return f"Out: {value}"


@app.callback(Output("debug-output", "children"), Input("sejm-plot", "hoverData"))
def test_click_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(Output("scatter_matrix", "figure"), Input("dropdown", "value"))
def update_bar_chart(dims):
    fig = get_scatter_matrix(dims)
    return fig
