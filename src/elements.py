import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import util

from dash import dcc, html, dash_table

from data import REPR_DF


PLOT_BG_COLOR = "rgb(240, 240, 240)"
HIST_DROPDOWN_TRANSLATION = {
    "List": "list",
    "Constituency": "constituency_city",
    "Votes Count": "votes_count",
    "Seniority": "seniority",
    "City of Birth": "city_of_birth",
    "Education": "education",
    "Occupation": "occupation",
    "Voting Participation": "voting_participation",
    "Cash in PLN": "cash_polish_currency",
    "Foreign Cash": "cash_foreign_currency",
    "Value of Other Shares": "other_shares_value",
    "Vehicles Count": "vehicles_count",
    "Debt": "loans_value",
    "Total Funds": "total_funds",
    "Number of Flats": "num_flats",
    "Number of Houses": "num_houses",
}


def get_nav_bar() -> html.Div:
    return html.Div(
        children=[
            html.Img(src="/assets/logos/put_logo.svg", height=80, width=300),
            html.H2("REPRESENTATIVES OF THE IX-th SEJM CADENCY", id="title"),
            html.Div(
                children=[
                    html.Button(
                        "By Individual",
                        id="individual-button",
                        className="nav-button",
                        n_clicks=0,
                    ),
                    html.Button(
                        "By Party",
                        id="party-button",
                        className="nav-button",
                        n_clicks=0,
                    ),
                    html.Button(
                        "By Feature",
                        id="feature-button",
                        className="nav-button",
                        n_clicks=0,
                    ),
                    html.Button(
                        "About Section",
                        id="about-button",
                        className="nav-button",
                        n_clicks=0,
                    ),
                ]
            ),
        ],
        className="nav-bar",
    )


def get_main_sejm_plot() -> dcc.Graph:
    x, y = util.generate_sejm_plot_rings()
    repr_seats_df = REPR_DF.copy()
    repr_seats_df["party_size"] = repr_seats_df.party_short.apply(
        lambda party: repr_seats_df.party_short.to_list().count(party)
    )
    repr_seats_df = repr_seats_df.sort_values(by="party_size")
    repr_seats_df["seat_x"] = x
    repr_seats_df["seat_y"] = y
    fig = px.scatter(
        repr_seats_df,
        x="seat_x",
        y="seat_y",
        color="party_short",
        custom_data=["name", "sejm_function", "academic_degree"],
        labels={"party_short": "Political Party"},
        width=900,
        height=450,
    )
    fig.update_traces(
        marker={"size": 15},
        hovertemplate="Name: %{customdata[0]}<br>Sejm function: %{customdata[1]}<br>Degree: %{customdata[2]}",
    )

    fig.update_layout(
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        xaxis=dict(showgrid=False, visible=False, zeroline=False, fixedrange=True),
        yaxis=dict(showgrid=False, visible=False, zeroline=False, fixedrange=True),
        title=dict(
            text="<b>Polish Sejm Split</b>",
            x=0.42,
            y=0.95,
            font=dict(family="Montserrat-Thin", size=30),
        ),
        margin=dict(l=20, b=20, r=20, t=80),
        paper_bgcolor=PLOT_BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
    )
    return dcc.Graph(
        id="sejm-plot",
        config={"displayModeBar": False, "autosizable": True, "responsive": True},
        figure=fig,
    )


def get_repr_data_section() -> html.Div:
    return html.Div(
        children=[
            html.H2("Choose a representative", id="repr-name"),
            html.Hr(style={"color": "white"}),
            html.H4(
                "For which the data should be displayed",
                id="repr-data",
            ),
        ],
        className="side-bar",
    )


def get_sejm_plot_section() -> html.Div:
    return html.Span(
        children=[
            html.Div(children=[get_main_sejm_plot()], className="sejm-plot-div"),
            get_repr_data_section(),
        ],
        className="sejm-plot section",
    )


def get_icon_entry(text: str, element_id: str) -> html.Div:
    return html.Div(
        children=[
            html.H2(text),
            html.Div(children=[], className="icon-array", id=element_id),
        ],
        className="icon-entry",
    )


def get_repr_vis_section() -> html.Div:
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id="repr-participation-plot", config={"displayModeBar": False}
                    ),
                    dcc.Graph(id="repr-votes-plot", config={"displayModeBar": False}),
                ],
                id="repr-other",
                className="repr-other",
            ),
            dcc.Graph(
                figure={}, id="repr-funds-breakup", config={"displayModeBar": False}
            ),
            html.Div(
                children=[
                    get_icon_entry("Houses:", "house-array"),
                    get_icon_entry("Flats:", "flat-array"),
                    get_icon_entry("Vehicles:", "car-array"),
                    get_icon_entry("Farms:", "farm-array"),
                    get_icon_entry("Experience:", "experience-array"),
                ],
                className="repr-stats-panel",
            ),
        ],
        className="repr-vis section",
    )


def get_scatter_matrix(dims):
    df = REPR_DF.copy()  # replace with your own data source
    df["paper_value"] = df["securites_value"] + df["other_shares_value"]
    df["property_value"] = df["house_value"]
    fig = px.scatter_matrix(
        df,
        dimensions=dims,
        color="party_short",
        labels={col: col.replace("_", " ") for col in df.columns},
        custom_data=[
            "name",
            "date_of_birth",
            "education",
            "cash_polish_currency",
            "cash_foreign_currency",
        ],
    )
    fig.update_traces(diagonal_visible=True)
    fig.update_traces(
        marker={"size": 8},
        hovertemplate="Name: %{customdata[0]}<br>Date of birth: %{customdata[1]}<br>Education: %{customdata[2]}",
    )
    fig.add_trace(go.Splom(showupperhalf=False))

    return fig


def get_icons_array(count: int, randomize_id: bool, icon_name: str, **kwargs):
    style_dict = dict(**kwargs)
    return [
        html.Img(
            src=f"/assets/icons/{icon_name}",
            className=f"{icon_name.split('.')[0]} icon",
            id=util.get_random_id() if randomize_id else i,
            style=util.inplace_update_dict_copy(style_dict, "--order", i),
        )
        for i in range(count)
    ]


def get_funds_fig(record):
    funds_breakup = util.get_repr_funds_breakup(record)
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
        paper_bgcolor=PLOT_BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
    )
    return funds_fig


def get_voting_participation_fig(vp_data: dict, color: str):
    vp_fig = px.bar(vp_data, x="val", y="label", orientation="h", text_auto=True)
    vp_fig.update_traces(marker=dict(color=[color]))
    vp_fig.update_layout(
        xaxis=dict(range=[0, 100], title=""),
        yaxis=dict(title=""),
        title=dict(
            text="<b>Participation in voting sessions [%]:</b>",
            font=dict(family="Montserrat-Thin", size=16),
        ),
        paper_bgcolor=PLOT_BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
        transition=dict(duration=1000),
    )
    return vp_fig


def get_votes_count_fig(vc_data: dict):
    vc_fig = px.bar(vc_data, x="val", y="label", orientation="h", text_auto=True)
    vc_fig.update_layout(
        xaxis=dict(range=[0, 500_000], title=""),
        yaxis=dict(title=""),
        title=dict(
            text="<b>Number of votes the representative has received:</b>",
            font=dict(family="Montserrat-Thin", size=16),
        ),
        paper_bgcolor=PLOT_BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
        transition=dict(duration=1000),
    )
    return vc_fig


def get_parties_fig():
    party_count_df = (
        REPR_DF.groupby(["party_full", "party_short", "list"], as_index=False)
        .count()[["party_full", "party_short", "list", "name"]]
        .rename(columns={"name": "repr_count"})
    )
    fig = px.sunburst(
        party_count_df,
        path=["party_short", "list"],
        values="repr_count",
        width=700,
        height=700,
    )
    fig.update_layout(
        title=dict(
            text="<b>Inner ring: Current political affiliation<br>Outer ring: List from which members started</b>",
            font=dict(family="Montserrat-Thin", size=20),
        ),
        paper_bgcolor=PLOT_BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
    )
    return fig


def get_base_sejm_data():
    base_sejm_data = [
        "Number of representatives: 460",
        "Total number of received votes: 11,399,592",
        "Average age: 52.6",
        "Average total funds: 1,392,234.46 PLN",
        "Average debt: 435,427.24 PLN",
    ]
    return html.Div(
        children=[
            html.H3("Sejm Rzeczypospolitej Polskiej"),
            html.Hr(style={"color": "white"}),
        ]
        + [html.H3(text) for text in base_sejm_data],
        className="party-details",
        id="party-details",
    )


def get_party_side_bar():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Img(src="/assets/logos/sejm.png", className="party-image")
                ],
                className="party-image-div",
                id="party-image-div",
            ),
            get_base_sejm_data(),
        ],
        id="party-side-bar",
        className="side-bar",
    )


def get_party_plot_section():
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id="party-plot",
                        figure=get_parties_fig(),
                        config={
                            "displayModeBar": False,
                            "autosizable": True,
                            "responsive": True,
                        },
                    ),
                ],
                className="party-plot-div",
            ),
            get_party_side_bar(),
        ],
        className="party-plot section",
    )


def get_party_stats_section():
    return html.Div(
        children=[
            html.Div(
                children=dcc.Graph(
                    id="party-histogram",
                    config={
                        "displayModeBar": False,
                        "autosizable": True,
                        "responsive": True,
                    },
                ),
                className="party-histogram-div",
            ),
            html.Div(
                children=[
                    html.H2("Select attriute distribution of which to plot:"),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                options=list(HIST_DROPDOWN_TRANSLATION.keys()),
                                id="party-stats-dropdown",
                            )
                        ]
                    ),
                ],
                className="party-stats side-bar",
            ),
        ],
        className="party-stats section",
    )


def get_histogram_fig(dataframe, value: str, selected: str):
    fig = px.histogram(
        dataframe, x=HIST_DROPDOWN_TRANSLATION[value], color="party_short"
    )
    fig.update_layout(
        title=dict(
            text=f"<b>Distribution of {value} for {selected}</b>",
            font=dict(family="Montserrat-Thin", size=16),
        ),
        paper_bgcolor=PLOT_BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
    )
    return fig


def get_bar_char(value):
    df = REPR_DF.copy()
    df["paper_value"] = df["securites_value"] + df["other_shares_value"]
    if value in [
        "cash_polish_currency",
        "cash_foreign_currency",
        "paper_value",
        "loans_value",
        "total_funds",
    ]:
        df[value].where(~((df[value] > 0) & (df[value] < 1000)), other=0, inplace=True)
        df[value].where(
            ~((df[value] > 1000) & (df[value] < 10000)), other=1000, inplace=True
        )
        df[value].where(
            ~((df[value] > 10000) & (df[value] < 100000)), other=10000, inplace=True
        )
        df[value].where(
            ~((df[value] > 100000) & (df[value] < 1000000)), other=100000, inplace=True
        )
        df[value].where(~(df[value] > 1000000), other=1000000, inplace=True)
        df[value] = df[value].fillna(0)
        df[value] = df[value].apply(str)

    new_df = pd.DataFrame(
        {"count": df.groupby(["party_short", value]).size()}
    ).reset_index()
    fig = px.bar(
        new_df,
        x=new_df.party_short,
        y=new_df["count"],
        color=new_df[value],
        title="Parties acording to " + value.replace("_", " "),
        labels={col: col.replace("_", " ") for col in df.columns},
    )
    fig.update_layout(yaxis=dict(title="Count"), xaxis=dict(title="Party"))
    return fig


def get_table(value):
    df = REPR_DF.copy()
    df = df.fillna(0)
    df["paper_value"] = df["securites_value"] + df["other_shares_value"]
    dict_rename = {
        "name": "Name",
        "party_short": "Party name",
        "education": "Education",
        "occupation": "Occupation",
        "vehicles_count": "Number of vehicles",
        "cash_polish_currency": "Cash in polish currency",
        "cash_foreign_currency": "Cash in foreign currency",
        "paper_value": "Total value in paper",
        "loans_value": "Total debt",
        "total_funds": "Total funds",
        "num_houses": "Number of houses",
        "num_flats": "Number of flats",
    }

    df.rename(columns=dict_rename, inplace=True)

    df = df[["Name", "Party name", dict_rename[value]]]
    table = dbc.Container(
        [
            dash_table.DataTable(
                id="datatable-interactivity",
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True}
                    for i in df.columns
                ],
                data=df.to_dict("records"),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=10,
            ),
            html.Div(id="datatable-interactivity-container"),
        ]
    )
    return table


def get_hidden_panel_content():
    displayed_df = REPR_DF[["name", "party_short"]].rename(
        columns={"name": "Name", "party_short": "Party"}
    )
    return dbc.Container(
        children=[
            html.H2("Representatives Datatable"),
            dash_table.DataTable(
                displayed_df.to_dict("records"),
                [{"name": i, "id": i} for i in ["Name", "Party"]],
                id="repr-table",
                fixed_rows={"headers": True},
                virtualization=True,
                style_as_list_view=True,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                style_cell={
                    "overflowX": "hidden",
                    "textOverflow": "ellipsis",
                    "width": "50%",
                },
                style_header={
                    "backgroundColor": "darkgray",
                    "fontWeight": "bold",
                    "color": "white",
                },
                style_table={"height": 350},
            ),
        ],
        fluid=True,
        id="table-container",
        class_name="table-container",
    )


def get_hidden_panel_elements():
    return (
        html.Button(">", id="table-panel-button", n_clicks=0),
        html.Div(
            children=[get_hidden_panel_content()],
            id="hidden-panel",
            className="hidden-panel",
        ),
        html.P(id="placeholder"),
    )
