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
        if (n_clicks == 0) {
            return;
        }
        show_hidden_panel();
    }
    """,
    Output("placeholder", "children"),
    Input("table-panel-button", "n_clicks"),
    prevent_initial_callback=True,
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
    Input("repr-table", "active_cell"),
    prevent_initial_callback=True,
)
def on_sejm_plot_clicked(repr_data, active_cell):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "sejm-plot" in changed_id:
        try:
            name = repr_data["points"][0]["customdata"][0]
        except TypeError:
            raise PreventUpdate()
    else:
        if not active_cell or active_cell["column_id"] != "Name":
            raise PreventUpdate()
        name = REPR_DF.loc[active_cell["row"], "name"]
    clicked_entry = next(REPR_DF.set_index("name").loc[[name]].fillna(0).itertuples())
    repr_data_format = """
    Political party: {party_full}
    City of birth: {city_of_birth}
    Date of birth: {date_of_birth}
    Constituency city: {constituency_city}
    Election list: {list}
    Total funds and estates value: {total_funds:,.2f} PLN
    Total loans value: {loans_value:,.2f} PLN
    """.format(
        **clicked_entry._asdict()
    )
    repr_data_format = repr_data_format.split("\n")
    repr_data_format = [html.H4(verse) for verse in repr_data_format]

    num_cars = int(clicked_entry.vehicles_count)
    num_farms = 1 if clicked_entry.farm_estate_size else 0
    num_houses = clicked_entry.num_houses
    num_flats = clicked_entry.num_flats

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


@app.callback(
    Output("party-image-div", "children"),
    Output("party-details", "children"),
    Input("party-plot", "clickData"),
)
def display_clicked_data(clickData):
    if clickData is None:
        raise PreventUpdate()
    point_dict = clickData["points"][0]
    if point_dict["parent"]:
        raise PreventUpdate()
    selected = point_dict["id"] if "root" in point_dict else "sejm"
    selected_data = util.get_selected_party_stats(selected, REPR_DF)
    full_name = (
        selected_data.party_full
        if selected != "sejm"
        else "Sejm Rzeczypospolitej Polskiej"
    )
    text = """
    Number of representatives: {name}
    Total number of received votes: {votes_count:,.0f}
    Average age: {age:.1f}
    Average total funds: {total_funds:,.2f} PLN
    Average debt: {loans_value:,.2f} PLN
    """.format(
        **selected_data._asdict()
    )
    return [
        html.Img(
            src=f"/assets/logos/{selected.replace('.', '')}.png",
            className="party-image",
        )
    ], [html.H3(full_name), html.Hr(style={"color": "white"})] + [
        html.H4(row) for row in text.split("\n")
    ]


@app.callback(
    Output("party-histogram", "figure"),
    Input("party-plot", "clickData"),
    Input("party-stats-dropdown", "value"),
)
def plot_histogram(clickData, value):
    if clickData is None or value is None:
        raise PreventUpdate()
    point_dict = clickData["points"][0]
    if point_dict["parent"]:
        raise PreventUpdate()
    repr_df = REPR_DF.copy()
    selected = point_dict["id"] if "root" in point_dict else "Sejm"
    if selected != "Sejm":
        repr_df = repr_df[repr_df.party_short == selected]
    fig = elements.get_histogram_fig(repr_df, value, selected)
    return fig


@app.callback(Output("bar-plot", "figure"), Input("dropdown-2", "value"))
def update_bar_chart(dims):
    fig = elements.get_bar_char(dims)
    return fig


@app.callback(Output("table", "children"), Input("dropdown-2", "value"))
def update_graphs(value):
    return elements.get_table(value)
