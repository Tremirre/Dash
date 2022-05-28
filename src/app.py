import plotly.express as px

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from elements import get_scatter_matrix
from data import REPR_DF
from util import sum_repr_funds, get_repr_funds_breakup

app = Dash(__name__)


@app.callback(
    [
        Output("repr-name", "children"),
        Output("repr-data", "children"),
        Output("car-array", "children"),
        Output("house-array", "children"),
        Output("flat-array", "children"),
        Output("farm-array", "children"),
        Output("experience-array", "children"),
        Output("repr-funds-breakup", "figure"),
    ],
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
    City of birth: {city_of_birth}\n
    Date of birth: {date_of_birth}\n
    Total funds and estates value: {total:,.2f} PLN\n
    Total loans value: {loans_value:,.2f} PLN
    """.format(
        **clicked_entry._asdict(), total=sum_repr_funds(clicked_entry)
    )
    repr_data_format = repr_data_format.split("\n")
    repr_data_format = [html.P(verse) for verse in repr_data_format]

    num_cars = int(clicked_entry.vehicles_count)
    num_farms = 1 if clicked_entry.farm_estate_size else 0
    num_houses = 0
    if not clicked_entry.house_size:
        if type(clicked_entry.house_size) is list:
            num_houses = len(clicked_entry.house_size)
        else:
            num_houses = 1
    num_flats = 0
    if not clicked_entry.flat_size:
        if type(clicked_entry.flat_size) is list:
            num_flats = len(clicked_entry.flat_size)
        else:
            num_flats = 1
    exp = clicked_entry.seniority

    car_icons = [
        html.Img(src="/assets/icons/car.svg", className="icon") for _ in range(num_cars)
    ]
    house_icons = [
        html.Img(src="/assets/icons/house.svg", className="icon")
        for _ in range(num_houses)
    ]
    flat_icons = [
        html.Img(src="/assets/icons/flat.svg", className="icon")
        for _ in range(num_flats)
    ]
    farm_icons = [
        html.Img(src="/assets/icons/farm.svg", className="icon")
        for _ in range(num_farms)
    ]
    exp_icons = [
        html.Img(src="/assets/icons/star.svg", className="star-icon")
        for _ in range(exp)
    ]

    funds_breakup = get_repr_funds_breakup(clicked_entry)
    funds_fig = px.pie(
        funds_breakup, values="Value", names="Asset", height=400, hole=0.4
    )
    funds_fig.update_traces(
        hovertemplate="Value: <b>%{value}PLN</b><br>Asset type: <b>%{label}</b>"
    )
    funds_fig.update_layout(
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        title=dict(
            text="<b>Funds Breakdown</b>",
            font=dict(family="Montserrat-Thin", size=24),
        ),
        margin=dict(l=20, b=20, r=20, t=80),
        paper_bgcolor="rgb(240, 240, 240)",
        plot_bgcolor="rgb(240, 240, 240)",
    )
    return (
        name,
        repr_data_format,
        car_icons,
        house_icons,
        flat_icons,
        farm_icons,
        exp_icons,
        funds_fig,
    )


@app.callback(Output("scatter_matrix", "figure"), Input("dropdown", "value"))
def update_bar_chart(dims):
    fig = get_scatter_matrix(dims)
    return fig
