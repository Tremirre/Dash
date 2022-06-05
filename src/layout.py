import elements

import dash_bootstrap_components as dbc
from dash import html, dcc

PAGE_1 = [
    elements.get_nav_bar(),
    *elements.get_hidden_panel_elements(),
    elements.get_sejm_plot_section(),
    elements.get_repr_vis_section(),
]

PAGE_2 = [
    elements.get_nav_bar(),
    elements.get_party_plot_section(),
    elements.get_party_stats_section(),
]

PAGE_3 = [
    elements.get_nav_bar(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(
        children=[
            html.H1("Select feature to analyse"),
            dcc.Dropdown(
                id="dropdown-2",
                options=[
                    "education",
                    "occupation",
                    "vehicles_count",
                    "cash_polish_currency",
                    "cash_foreign_currency",
                    "paper_value",
                    "loans_value",
                    "total_funds",
                    "num_houses",
                    "num_flats",
                ],
                value="education",
                multi=False,
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        config={
                            "displayModeBar": False,
                            "autosizable": True,
                            "responsive": True,
                        },
                        id="bar-plot",
                    )
                ]
            ),
            html.Div(children=[dbc.Container(id="table")]),
        ]
    ),
    html.P(id="placeholder"),
]

PAGE_4 = [
    elements.get_nav_bar(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H1("About"),
    html.H2("Data"),
    html.H3("https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp"),
    html.H3("This dashboard is based on manually collected data and the correctness of this data is not guaranteed. "
            "The data were written down from the declarations of assets of deputies and other data provided on the "
            "official website of the Sejm."),
    html.H2("By Individual"),
    html.H3("In this section we can see the distribution of the Sejm by party. Each Member shall be represented by a "
            "single point. After selecting the point on the right, we are shown detailed information about the "
            "Member. "),
    html.H2("By Party"),
    html.H3("On this page we can see a pie chart with parties represented in the Polish Parliament. After selecting a "
            "given batch, detailed data on a given batch appear to us. Additional below we have the opportunity to "
            "see how the deputies of a given party present themselves numerically according to the selected "
            "attribute."),
    html.H2("By Feature"),
    html.H3("With this page we can select an attribute and compare it between batches. In addition, we have a board "
            "that represents MPs together with the selected attribute. You can filter and search for data in the "
            "selected column."),


    html.H3()
]