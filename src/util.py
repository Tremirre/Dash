import numpy as np


def get_circle_points(radius: float, arc_length: float, max_points: int) -> tuple[list[float], list[float]]:
    X = []
    Y = []
    cur_angle = 0
    angle_change = arc_length/radius
    expected = int(np.pi / angle_change)
    unused = np.fmod(np.pi, angle_change)
    angle_change += unused / expected
    while cur_angle <= np.pi + unused and len(X) < max_points:
        X.append(np.cos(cur_angle) * radius)
        Y.append(np.sin(cur_angle) * radius)
        cur_angle += angle_change
    return X, Y


def generate_sejm_plot_rings(arc_length = 0.45, r_0 = 1.6, dr = 0.8, num_points = 460):
    X = []
    Y = []
    while num_points - len(X) > 0:
        x, y = get_circle_points(r_0, arc_length, num_points - len(X))
        X.extend(x)
        Y.extend(y)
        r_0 += dr
    sorted_by_angle = sorted([(x, y, np.arctan2(y, x)) for x, y in zip(X, Y)], key=lambda x: x[2])
    X, Y, _ = list(zip(*sorted_by_angle))
    return X, Y