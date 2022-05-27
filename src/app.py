from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from elements import get_scatter_matrix
from data import REPR_DF
from util import sum_repr_funds

app = Dash(__name__)


@app.callback(
    [Output("repr-name", "children"), Output("repr-data", "children")],
    Input("sejm-plot", "clickData"),
    prevent_initial_callback=True,
)
def test_click_data(repr_data):
    try:
        name = repr_data["points"][0]["customdata"][0]
    except TypeError:
        raise PreventUpdate()
    clicked_entry = next(REPR_DF.set_index("name").loc[[name]].fillna(0).itertuples())
    repr_data_format = """
    Election list: {list}\n
    Political party: {party_full}\n
    Constituency city: {constituency_city}\n
    Votes count: {votes_count}\n
    Experiance as a representative: {seniority} cadencies\n
    City of birth: {city_of_birth}\n
    Date of birth: {date_of_birth}\n
    Total funds and estates value: {total:.2f} PLN\n
    Total loans value: {loans_value:.2f} PLN
    """.format(
        **clicked_entry._asdict(), total=sum_repr_funds(clicked_entry)
    )
    repr_data_format = repr_data_format.split("\n")
    repr_data_format = [html.P(verse) for verse in repr_data_format]
    return name, repr_data_format


@app.callback(Output("scatter_matrix", "figure"), Input("dropdown", "value"))
def update_bar_chart(dims):
    fig = get_scatter_matrix(dims)
    return fig
