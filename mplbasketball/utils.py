import numpy as np


def transform(x, y, fr, to, origin, court_dims=[94.0, 50.0]):
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
    - court_dims: list
        Dimensions of the court. Default is [94.0, 50.0].

    Returns:
    --------
    - x: np.array
        Transformed x-coordinates.
    - y: np.array
        Transformed y-coordinates.
    """

    if origin == "center":
        center_court = [0.0, 0.0]
    elif origin == "top-left":
        center_court = [court_dims[0] / 2, -court_dims[1] / 2]
    elif origin == "bottom-left":
        center_court = [court_dims[0] / 2, court_dims[1] / 2]
    elif origin == "top-right":
        center_court = [-court_dims[0] / 2, -court_dims[1] / 2]
    elif origin == "bottom-right":
        center_court = [-court_dims[0] / 2, court_dims[1] / 2]

    if fr == to:
        return x, y

    else:
        if fr[0] == "h" and to[0] == "h":
            x_t = x.copy()
            if (fr == "h" or fr == "hl") and to == "hr":
                x[x_t < center_court[0]] = 2 * center_court[0] - x[x_t < center_court[0]]
                y[x_t < center_court[0]] = 2 * center_court[1] - y[x_t < center_court[0]]
            elif (fr == "h" or fr == "hr") and to == "hl":
                x[x_t > center_court[0]] = 2 * center_court[0] - x[x_t > center_court[0]]
                y[x_t > center_court[0]] = 2 * center_court[1] - y[x_t > center_court[0]]
        elif fr[0] == "v" and to[0] == "v":
            y_t = y.copy()
            if (fr == "v" or fr == "vl") and to == "vu":
                x[y_t < center_court[0]] = -2 * center_court[1] - x[y_t < center_court[0]]
                y[y_t < center_court[0]] = 2 * center_court[0] - y[y_t < center_court[0]]
            elif (fr == "v" or fr == "vu") and to == "vd":
                x[y > center_court[0]] = -2 * center_court[1] - x[y > center_court[0]]
                y[y > center_court[0]] = 2 * center_court[0] - y[y > center_court[0]]
        elif fr[0] == "h" and to[0] == "v":
            x_t = x.copy()
            y_t = y.copy()
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
            x_t = x.copy()
            y_t = y.copy()
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
