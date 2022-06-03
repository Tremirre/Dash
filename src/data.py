import pandas as pd

from pathlib import Path

REPR_DF = pd.read_pickle(
    f"{Path(__file__).absolute().parent.parent}/data/repr_processed.pickle"
)
