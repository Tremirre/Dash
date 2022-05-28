import numpy as np


def get_circle_points(
    radius: float, arc_length: float, max_points: int
) -> tuple[list[float], list[float]]:
    X = []
    Y = []
    cur_angle = 0
    angle_change = arc_length / radius
    expected = int(np.pi / angle_change)
    unused = np.fmod(np.pi, angle_change)
    angle_change += unused / expected
    while cur_angle <= np.pi + unused and len(X) < max_points:
        X.append(np.cos(cur_angle) * radius)
        Y.append(np.sin(cur_angle) * radius)
        cur_angle += angle_change
    return X, Y


def generate_sejm_plot_rings(arc_length=0.45, r_0=1.6, dr=0.8, num_points=460):
    X = []
    Y = []
    while num_points - len(X) > 0:
        x, y = get_circle_points(r_0, arc_length, num_points - len(X))
        X.extend(x)
        Y.extend(y)
        r_0 += dr
    sorted_by_angle = sorted(
        [(x, y, np.arctan2(y, x)) for x, y in zip(X, Y)], key=lambda x: x[2]
    )
    X, Y, _ = list(zip(*sorted_by_angle))
    return X, Y


def sum_repr_funds(repr) -> float:
    cash_pl = repr.cash_polish_currency
    cash_fg = repr.cash_foreign_currency
    securities = repr.securites_value
    house_value = repr.house_value
    flat_value = repr.flat_value
    farm_estate_value = repr.farm_estate_value
    other_estates_value = repr.other_estates_value
    other_shares_value = repr.other_shares_value
    if type(house_value) is list:
        house_value = sum(house_value)
    if type(flat_value) is list:
        flat_value = sum(flat_value)
    return sum(
        [
            cash_pl,
            cash_fg,
            securities,
            house_value,
            flat_value,
            farm_estate_value,
            other_estates_value,
            other_shares_value,
        ]
    )


def get_repr_funds_breakup(record):
    cash_pl = record.cash_polish_currency
    cash_fg = record.cash_foreign_currency
    securities = record.securites_value
    house_value = record.house_value
    flat_value = record.flat_value
    farm_estate_value = record.farm_estate_value
    other_estates_value = record.other_estates_value
    other_shares_value = record.other_shares_value
    if type(house_value) is list:
        house_value = sum(house_value)
    if type(flat_value) is list:
        flat_value = sum(flat_value)
    values = [
        cash_pl,
        cash_fg,
        securities,
        house_value,
        flat_value,
        farm_estate_value,
        other_estates_value,
        other_shares_value,
    ]
    values = [val if val > 0 else None for val in values]
    return {
        "Asset": [
            "Cash in PLN",
            "Cash in foreing currencies",
            "Value of securities",
            "Value of houses",
            "Value of flats",
            "Value of farms",
            "Value of other estates",
            "Value of other shares",
        ],
        "Value": values,
    }
