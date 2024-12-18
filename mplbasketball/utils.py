from typing import Literal

import numpy as np

from mplbasketball.court_params import _get_court_params_in_desired_units


def transform(
    x: np.ndarray,
    y: np.ndarray,
    fr: Literal["h", "hl", "hr", "v", "vu", "vd"],
    to: Literal["h", "hl", "hr", "v", "vu", "vd"],
    origin: Literal["center", "top-left", "bottom-left", "top-right", "bottom-right"],
    court_type: Literal["nba", "wnba", "ncaa", "fiba"] = "nba",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Function to transform a set of x, y values to match orientations desired for plotting.

    Parameters:
    -----------
    - x: np.array
        x-coordinates of the data points.
    - y: np.array
        y-coordinates of the data points.
    - fr: str
        Current orientation of the data points. Can be one of 'h', 'hl', 'hr', 'v', 'vu', 'vd'.
    - to: str
        Desired orientation of the data points. Can be one of 'h', 'hl', 'hr', 'v', 'vu', 'vd'.
    - origin: str
        Origin of the court. Can be one of 'center', 'top-left', 'bottom-left', 'top-right', 'bottom-right'.
    - court_type: str
        Court type. Can be one of 'nba', 'wnba', 'ncaa', 'fiba'.

    Returns:
    --------
    - x: np.array
        Transformed x-coordinates.
    - y: np.array
        Transformed y-coordinates.
    """
    # Validate inputs
    if fr not in ["h", "hl", "hr", "v", "vu", "vd"]:
        raise ValueError(f"Invalid value for 'fr': {fr}")
    if to not in ["h", "hl", "hr", "v", "vu", "vd"]:
        raise ValueError(f"Invalid value for 'to': {to}")
    if origin not in ["center", "top-left", "bottom-left", "top-right", "bottom-right"]:
        raise ValueError(f"Invalid value for 'origin': {origin}")
    if court_type not in ["nba", "wnba", "ncaa", "fiba"]:
        raise ValueError(f"Invalid value for 'court_type': {court_type}")

    # Retrieve court parameters
    court_params = _get_court_params_in_desired_units(court_type, "ft")
    court_dims = court_params["court_dims"]

    # Calculate center based on origin
    origins = {
        "center": [0.0, 0.0],
        "top-left": [court_dims[0] / 2, -court_dims[1] / 2],
        "bottom-left": [court_dims[0] / 2, court_dims[1] / 2],
        "top-right": [-court_dims[0] / 2, -court_dims[1] / 2],
        "bottom-right": [-court_dims[0] / 2, court_dims[1] / 2],
    }
    center_court = origins[origin]

    if fr == to:
        return x, y

    else:
        x_t, y_t = x.copy(), y.copy()

        if fr[0] == "h" and to[0] == "h":
            if (fr == "h" or fr == "hl") and to == "hr":
                x[x_t < center_court[0]] = 2 * center_court[0] - x[x_t < center_court[0]]
                y[x_t < center_court[0]] = 2 * center_court[1] - y[x_t < center_court[0]]
            elif (fr == "h" or fr == "hr") and to == "hl":
                x[x_t > center_court[0]] = 2 * center_court[0] - x[x_t > center_court[0]]
                y[x_t > center_court[0]] = 2 * center_court[1] - y[x_t > center_court[0]]

        elif fr[0] == "v" and to[0] == "v":
            if (fr == "v" or fr == "vl") and to == "vu":
                x[y_t < center_court[0]] = -2 * center_court[1] - x[y_t < center_court[0]]
                y[y_t < center_court[0]] = 2 * center_court[0] - y[y_t < center_court[0]]
            elif (fr == "v" or fr == "vu") and to == "vd":
                x[y > center_court[0]] = -2 * center_court[1] - x[y > center_court[0]]
                y[y > center_court[0]] = 2 * center_court[0] - y[y > center_court[0]]

        elif fr[0] == "h" and to[0] == "v":
            if to[0] == "v":  # Works for any of 'h', 'hl', 'hr'
                x = -y_t
                y = x_t
                if to == "vu":
                    x[y < center_court[0]] = -2 * center_court[1] - x[y < center_court[0]]
                    y[y < center_court[0]] = 2 * center_court[0] - y[y < center_court[0]]
                elif to == "vd":
                    x[y > center_court[0]] = -2 * center_court[1] - x[y > center_court[0]]
                    y[y > center_court[0]] = 2 * center_court[0] - y[y > center_court[0]]

        elif fr[0] == "v" and to[0] == "h":
            if to[0] == "h":  # Works for any of 'v', 'vu', 'vd'
                x = y_t
                y = -x_t
                if to == "hr":
                    x[x < center_court[0]] = 2 * center_court[0] - x[x < center_court[0]]
                    y[x < center_court[0]] = 2 * center_court[1] - y[x < center_court[0]]
                elif to == "hl":
                    x[x > center_court[0]] = 2 * center_court[0] - x[x > center_court[0]]
                    y[x > center_court[0]] = 2 * center_court[1] - y[x > center_court[0]]

        return x, y
