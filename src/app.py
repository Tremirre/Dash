import plotly.express as px

import util
import elements
import layout

from dash import Dash, html, dcc, callback_context
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from data import REPR_DF

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

app.clientside_callback(
    """
    function(n_clicks) {
        return;
    }
    """,
    Output("placeholder", "children"),
    Input("test-button", "n_clicks"),
)


@app.callback(
    Output("page-layout", "children"),
    Input("individual-button", "n_clicks"),
    Input("party-button", "n_clicks"),
    Input("about-button", "n_clicks"),
    Input("test-button", "n_clicks"),
)
def page_changer(*args):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "party-button" in changed_id:
        return layout.PAGE_2
    if "test-button" in changed_id:
        return layout.PAGE_3
    return layout.PAGE_1


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
        Output("repr-participation-plot", "figure"),
        Output("repr-votes-plot", "figure"),
    ],
    Input("sejm-plot", "clickData"),
    prevent_initial_callback=True,
)
def on_sejm_plot_clicked(repr_data):
    try:
        name = repr_data["points"][0]["customdata"][0]
    except TypeError:
        raise PreventUpdate()
    clicked_entry = next(REPR_DF.set_index("name").loc[[name]].fillna(0).itertuples())
    repr_data_format = """
    Election list: {list}\n
    Political party: {party_full}\n
    Constituency city: {constituency_city}\n
    City of birth: {city_of_birth}\n
    Date of birth: {date_of_birth}\n
    Total funds and estates value: {total:,.2f} PLN\n
    Total loans value: {loans_value:,.2f} PLN
    """.format(
        **clicked_entry._asdict(), total=util.sum_repr_funds(clicked_entry)
    )
    repr_data_format = repr_data_format.split("\n")
    repr_data_format = [html.P(verse) for verse in repr_data_format]

    num_cars = int(clicked_entry.vehicles_count)
    num_farms = 1 if clicked_entry.farm_estate_size else 0
    num_houses = util.get_count_from_estate_field(clicked_entry.house_size)
    num_flats = util.get_count_from_estate_field(clicked_entry.flat_size)

    exp = clicked_entry.seniority
    flat_width = min(50, 270 // (num_flats if num_flats > 0 else 1))
    car_icons = elements.get_icons_array(
        num_cars, randomize_id=True, icon_name="car.svg"
    )
    house_icons = elements.get_icons_array(
        num_houses, randomize_id=True, icon_name="house.svg"
    )
    flat_icons = elements.get_icons_array(
        num_flats, randomize_id=True, icon_name="flat.svg", width=f"{flat_width}px"
    )
    farm_icons = elements.get_icons_array(
        num_farms, randomize_id=True, icon_name="farm.svg"
    )
    exp_icons = elements.get_icons_array(exp, randomize_id=True, icon_name="star.svg")

    funds_fig = elements.get_funds_fig(clicked_entry)

    vp_data = {"val": [clicked_entry.voting_participation], "label": [""]}
    color = util.get_color_from_value(clicked_entry.voting_participation)
    vp_fig = elements.get_voting_participation_fig(vp_data, color)
    vc_data = {"val": [clicked_entry.votes_count], "label": [""]}
    vc_fig = elements.get_votes_count_fig(vc_data)

    return (
        name,
        repr_data_format,
        car_icons,
        house_icons,
        flat_icons,
        farm_icons,
        exp_icons,
        funds_fig,
        vp_fig,
        vc_fig,
    )


@app.callback(Output("scatter_matrix", "figure"), Input("dropdown", "value"))
def update_bar_chart(dims):
    fig = elements.get_scatter_matrix(dims)
    return fig
