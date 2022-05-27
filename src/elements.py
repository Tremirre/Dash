import pandas as pd
from regex import D
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

from dash import dcc, html

from util import generate_sejm_plot_rings
from data import REPR_DF


def get_main_sejm_plot():
    x, y = generate_sejm_plot_rings()
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
        custom_data=["name", "date_of_birth", "education"],
        labels={"party_short": "Political Party"},
        width=1000,
        height=500,
    )
    fig.update_traces(
        marker={"size": 15},
        hovertemplate="Name: %{customdata[0]}<br>Date of birth: %{customdata[1]}<br>Education: %{customdata[2]}",
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
    return dcc.Graph(id="sejm-plot", config={"displayModeBar": False}, figure=fig)


def get_repr_data_section():
    return html.Div(
        children=[html.H2(id="repr-name"), html.P(id="repr-data")],
        className="side-bar",
    )


def get_sejm_plot_section():
    return html.Div(
        children=[get_main_sejm_plot(), get_repr_data_section()],
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


def get_repr_vis_section():
    return html.Div(
        children=[
            html.Div(
                children=[
                    get_icon_entry("Houses:", "house-array"),
                    get_icon_entry("Flats:", "flat-array"),
                    get_icon_entry("Vehicles:", "car-array"),
                    get_icon_entry("Farm:", "farm-array"),
                    get_icon_entry("Experience:", "experience-array"),
                ]
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
