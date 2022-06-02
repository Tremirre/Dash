import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

import util

from dash import dcc, html

from data import REPR_DF


def get_nav_bar() -> html.Div:
    return html.Div(
        children=[
            html.Img(src="/assets/logos/put_logo.svg", height=80, width=300),
            html.H2("REPRESENTATIVES OF THE IX-th SEJM CADENCY", id="title"),
            html.Div(children=[html.Button("Execute", id="test-button", n_clicks=0)]),
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
        paper_bgcolor="rgb(240, 240, 240)",
        plot_bgcolor="rgb(240, 240, 240)",
    )
    return dcc.Graph(
        id="sejm-plot",
        config={"displayModeBar": False, "autosizable": True, "responsive": True},
        figure=fig,
    )


def get_repr_data_section() -> html.Div:
    return html.Div(
        children=[html.H2(id="repr-name"), html.P(id="repr-data")],
        className="side-bar",
    )


def get_sejm_plot_section() -> html.Div:
    return html.Span(
        children=[
            html.Div(children=[get_main_sejm_plot()], className="sejm-plot-div"),
            get_repr_data_section(),
        ],
        className="sejm-plot-section",
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
            dcc.Graph(id="repr-funds-breakup", config={"displayModeBar": False}),
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
        className="repr-vis-section",
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
        paper_bgcolor="rgb(240, 240, 240)",
        plot_bgcolor="rgb(240, 240, 240)",
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
        paper_bgcolor="rgb(240, 240, 240)",
        plot_bgcolor="rgb(240, 240, 240)",
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
        paper_bgcolor="rgb(240, 240, 240)",
        plot_bgcolor="rgb(240, 240, 240)",
        transition=dict(duration=1000),
    )
    return vc_fig
