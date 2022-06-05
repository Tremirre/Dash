import pandas as pd

from pathlib import Path

REPR_DF = pd.read_pickle(
    f"{Path(__file__).absolute().parent.parent}/data/repr_processed.pickle"
)

# Color 'kinda' associated with the party
PARTIES_COLOR_SCHEME = {
    "niez.": "dodgerblue",
    "PPS": "red",
    "Kukiz15": "black",
    "PS": "cadetblue",
    "Porozumienie": "violet",
    "Polska2050": "palegoldenrod",
    "Konfederacja": "midnightblue",
    "KP": "limegreen",
    "Lewica": "purple",
    "KO": "orange",
    "PiS": "blue",
}


# Default plotly color palette with fixed assignments
ASSETS_COLOR_SCHEME = {
    "Cash in PLN": "#636EFA",
    "Cash in foreign currencies": "#19D3F3",
    "Value of securities": "#FFA15A",
    "Value of houses": "#AB63FA",
    "Value of flats": "#00CC96",
    "Value of farms": "#EF553B",
    "Value of other estates": "#B6E880",
    "Value of other shares": "#FECB52",
}
