import dash_html_components as html
import dash_core_components as dcc

from dash import Dash
from dash.dependencies import Input, Output

app = Dash(__name__)

@app.callback(
        Output(component_id="test_output", component_property="children"),
        Input(component_id="test_input", component_property="value")
    )
def update_test_output(value):
    return f"Out: {value}" 