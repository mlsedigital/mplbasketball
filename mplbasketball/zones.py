from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Tuple, List

import numpy as np

from .court_params import _get_court_params_in_desired_units

Orientation = Literal["h", "v"]
Half = Literal["l", "r", "u", "d", None]
Origin = Literal["center", "top-left", "bottom-left", "top-right", "bottom-right"]
CourtType = Literal["nba", "wnba", "ncaa", "fiba"]
Units = Literal["ft", "m"]


@dataclass(frozen=True)
class CourtSpec:
    court_type: CourtType = "nba"
    units: Units = "ft"
    origin: Origin = "top-left"
    orientation: Orientation = "h"

    @property
    def params(self) -> dict:
        return _get_court_params_in_desired_units(self.court_type, self.units)

    @property
    def dims(self) -> Tuple[float, float]:
        p = self.params
        return float(p["court_dims"][0]), float(p["court_dims"][1])

    @property
    def center(self) -> Tuple[float, float]:
        cx, cy = _center_from_origin(self.origin, self.dims)
        if self.orientation == "h":
            return cx, cy
        else:
            # Rotate h -> v: (x, y) -> (-y, x)
            return -cy, cx

    @property
    def hoop_centers(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        # Compute in horizontal frame, then rotate to desired orientation
        params = self.params
        court_x, court_y = self.dims
        cx, cy = _center_from_origin(self.origin, self.dims)
        left_x = cx - court_x / 2 + params["hoop_distance_from_edge"]
        right_x = cx + court_x / 2 - params["hoop_distance_from_edge"]
        left = np.array([left_x, cy])
        right = np.array([right_x, cy])
        if self.orientation == "v":
            left = _h2v_point(*left)
            right = _h2v_point(*right)
        return (float(left[0]), float(left[1])), (float(right[0]), float(right[1]))


# -----------------------------
# Helpers
# -----------------------------

def _center_from_origin(origin: Origin, dims: Tuple[float, float]) -> Tuple[float, float]:
    w, h = dims
    if origin == "center":
        return 0.0, 0.0
    if origin == "top-left":
        return w / 2.0, -h / 2.0
    if origin == "bottom-left":
        return w / 2.0, h / 2.0
    if origin == "top-right":
        return -w / 2.0, -h / 2.0
    if origin == "bottom-right":
        return -w / 2.0, h / 2.0
    raise ValueError(f"Invalid origin: {origin}")


def _h2v_points(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # Horizontal -> Vertical rotation used by Court: (x, y) -> (-y, x)
    return -y, x


def _v2h_points(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # Vertical -> Horizontal inverse rotation: (x, y) -> (y, -x)
    return y, -x


def _h2v_point(x: float, y: float) -> np.ndarray:
    return np.array([-y, x], dtype=float)


# -----------------------------
# Geometry: polygons (numpy arrays of shape (N, 2))
# -----------------------------

def restricted_area_polygon(spec: CourtSpec, side: Literal["l", "r"], n: int = 128) -> np.ndarray:
    """Semicircle under the basket (charge circle). Returns a closed polygon.

    - side: 'l' (left) or 'r' (right) with respect to horizontal orientation.
            If spec.orientation == 'v', coordinates are rotated accordingly.
    """
    p = spec.params
    r = float(p["charge_circle_radius"])  # 4ft NBA
    (lx, ly), (rx, ry) = spec.hoop_centers
    cx, cy = (lx, ly) if side == "l" else (rx, ry)

    # Build in the target orientation directly
    # Determine opening direction unit vector: in 'h', left opens to +x, right opens to -x
    if spec.orientation == "h":
        theta1, theta2 = (-90.0, 90.0) if side == "l" else (90.0, -90.0)
    else:  # 'v'
        # In vertical view, 'down' basket corresponds to left; match Court arcs
        theta1, theta2 = (-90.0, 90.0) if side in ("l", "d") else (90.0, -90.0)

    thetas = np.linspace(np.deg2rad(theta1), np.deg2rad(theta2), n)
    xs = cx + r * np.cos(thetas)
    ys = cy + r * np.sin(thetas)
    # Close by chord
    poly = np.vstack([np.column_stack([xs, ys]), np.array([[xs[0], ys[0]]])])
    return poly


def paint_polygon(spec: CourtSpec, side: Literal["l", "r"]) -> np.ndarray:
    """Outer paint rectangle for a given side. Returns a closed polygon."""
    p = spec.params
    court_x, court_y = spec.dims
    center_x, center_y = spec.center
    w, h = float(p["outer_paint_dims"][0]), float(p["outer_paint_dims"][1])

    if spec.orientation == "h":
        if side == "l":
            x0 = center_x - court_x / 2.0
        else:
            x0 = center_x + court_x / 2.0 - w
        y0 = center_y - h / 2.0
        rect = np.array([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h], [x0, y0]], dtype=float)
        return rect
    else:
        # Build in H then rotate to V for consistency
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
        rect_h = paint_polygon(spec_h, side)
        xv, yv = _h2v_points(rect_h[:, 0], rect_h[:, 1])
        return np.column_stack([xv, yv])


def corner_three_rects(spec: CourtSpec, side: Literal["l", "r"]) -> List[np.ndarray]:
    """Top and bottom corner-three rectangles for a given side (closed polygons)."""
    p = spec.params
    court_x, court_y = spec.dims
    center_x, center_y = spec.center

    line_len = float(p["three_point_line_length"])  # along x from baseline
    side_w = float(p["three_point_side_width"])    # distance from sidelines

    if spec.orientation == "h":
        if side == "l":
            x0 = center_x - court_x / 2.0
            x1 = x0 + line_len
        else:
            x1 = center_x + court_x / 2.0
            x0 = x1 - line_len
        # Top rect
        yt0 = center_y + court_y / 2.0 - side_w
        yt1 = center_y + court_y / 2.0
        top = np.array([[x0, yt0], [x1, yt0], [x1, yt1], [x0, yt1], [x0, yt0]], dtype=float)
        # Bottom rect
        yb0 = center_y - court_y / 2.0
        yb1 = center_y - court_y / 2.0 + side_w
        bot = np.array([[x0, yb0], [x1, yb0], [x1, yb1], [x0, yb1], [x0, yb0]], dtype=float)
        return [top, bot]
    else:
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
        rects_h = corner_three_rects(spec_h, side)
        out: List[np.ndarray] = []
        for poly in rects_h:
            xv, yv = _h2v_points(poly[:, 0], poly[:, 1])
            out.append(np.column_stack([xv, yv]))
        return out


def three_point_arc_points(spec: CourtSpec, side: Literal["l", "r"], n: int = 256) -> np.ndarray:
    """Polyline along the three-point arc (not closed)."""
    p = spec.params
    (lx, ly), (rx, ry) = spec.hoop_centers
    center = (lx, ly) if side == "l" else (rx, ry)
    arc_angle = float(p["three_point_arc_angle"])  # degrees
    radius = float(p["three_point_arc_diameter"]) / 2.0

    if spec.orientation == "h":
        # In horizontal view, left arc is centered around 0°, right arc around 180°
        base1, base2 = -arc_angle, arc_angle
        offset = 0.0 if side == "l" else 180.0
    else:
        # Build in H then rotate
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
        pts_h = three_point_arc_points(spec_h, side, n)
        xv, yv = _h2v_points(pts_h[:, 0], pts_h[:, 1])
        return np.column_stack([xv, yv])

    thetas = np.deg2rad(np.linspace(base1 + offset, base2 + offset, n))
    cx, cy = center
    xs = cx + radius * np.cos(thetas)
    ys = cy + radius * np.sin(thetas)
    return np.column_stack([xs, ys])


# -----------------------------
# Zone membership masks (boolean)
# -----------------------------

def restricted_area_mask(
    x: np.ndarray,
    y: np.ndarray,
    spec: CourtSpec,
    side: Literal["l", "r", "both"] = "both",
) -> np.ndarray:
    """Points inside the no-charge (restricted) semicircle in front of hoop.

    Semicircle is defined by radius = charge_circle_radius centered at each hoop,
    and only the half facing midcourt is included.
    """
    # Ensure arrays
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Convert to horizontal frame for side logic; compute mask; then return
    if spec.orientation == "v":
        xh, yh = _v2h_points(x, y)
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
    else:
        xh, yh = x, y
        spec_h = spec

    p = spec_h.params
    r = float(p["charge_circle_radius"])
    (lx, ly), (rx, ry) = spec_h.hoop_centers

    dl2 = (xh - lx) ** 2 + (yh - ly) ** 2
    dr2 = (xh - rx) ** 2 + (yh - ry) ** 2

    # In front of hoop: for left, x >= lx; for right, x <= rx
    left_mask = (dl2 <= r * r) & (xh >= lx)
    right_mask = (dr2 <= r * r) & (xh <= rx)

    if side == "l":
        m = left_mask
    elif side == "r":
        m = right_mask
    else:
        m = left_mask | right_mask

    return m


def paint_mask(
    x: np.ndarray,
    y: np.ndarray,
    spec: CourtSpec,
    side: Literal["l", "r", "both"] = "both",
) -> np.ndarray:
    """Points inside the outer paint rectangles (per side or both)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if spec.orientation == "v":
        xh, yh = _v2h_points(x, y)
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
    else:
        xh, yh = x, y
        spec_h = spec

    p = spec_h.params
    court_x, court_y = spec_h.dims
    cx, cy = _center_from_origin(spec_h.origin, spec_h.dims)
    w, h = float(p["outer_paint_dims"][0]), float(p["outer_paint_dims"][1])

    # Left paint bounds
    xl0 = cx - court_x / 2.0
    xl1 = xl0 + w
    yl0 = cy - h / 2.0
    yl1 = cy + h / 2.0

    # Right paint bounds
    xr1 = cx + court_x / 2.0
    xr0 = xr1 - w
    yr0 = yl0
    yr1 = yl1

    left = (xh >= xl0) & (xh <= xl1) & (yh >= yl0) & (yh <= yl1)
    right = (xh >= xr0) & (xh <= xr1) & (yh >= yr0) & (yh <= yr1)

    if side == "l":
        m = left
    elif side == "r":
        m = right
    else:
        m = left | right

    return m


def corner_three_mask(
    x: np.ndarray,
    y: np.ndarray,
    spec: CourtSpec,
    side: Literal["l", "r", "both"] = "both",
) -> np.ndarray:
    """Points in the corner-three rectangles (top and bottom corners)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if spec.orientation == "v":
        xh, yh = _v2h_points(x, y)
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
    else:
        xh, yh = x, y
        spec_h = spec

    p = spec_h.params
    court_x, court_y = spec_h.dims
    cx, cy = _center_from_origin(spec_h.origin, spec_h.dims)

    line_len = float(p["three_point_line_length"])
    side_w = float(p["three_point_side_width"])

    # Left bounds
    xl0 = cx - court_x / 2.0
    xl1 = xl0 + line_len
    # Right bounds
    xr1 = cx + court_x / 2.0
    xr0 = xr1 - line_len

    # Top and bottom y bands
    top_band = (yh >= (cy + court_y / 2.0 - side_w)) & (yh <= (cy + court_y / 2.0))
    bot_band = (yh >= (cy - court_y / 2.0)) & (yh <= (cy - court_y / 2.0 + side_w))

    left = ((xh >= xl0) & (xh <= xl1)) & (top_band | bot_band)
    right = ((xh >= xr0) & (xh <= xr1)) & (top_band | bot_band)

    if side == "l":
        m = left
    elif side == "r":
        m = right
    else:
        m = left | right

    return m


def above_break_three_mask(
    x: np.ndarray,
    y: np.ndarray,
    spec: CourtSpec,
    side: Literal["l", "r", "both"] = "both",
) -> np.ndarray:
    """Points in the above-the-break three zone (outside the arc, excluding corners)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if spec.orientation == "v":
        xh, yh = _v2h_points(x, y)
        spec_h = CourtSpec(spec.court_type, spec.units, spec.origin, "h")
    else:
        xh, yh = x, y
        spec_h = spec

    p = spec_h.params
    cx, cy = _center_from_origin(spec_h.origin, spec_h.dims)
    court_x, court_y = spec_h.dims
    (lx, ly), (rx, ry) = spec_h.hoop_centers

    arc_r = float(p["three_point_arc_diameter"]) / 2.0
    side_w = float(p["three_point_side_width"])

    # Within central band (exclude corners)
    central_band = np.abs(yh - cy) <= (court_y / 2.0 - side_w)

    dl2 = (xh - lx) ** 2 + (yh - ly) ** 2
    dr2 = (xh - rx) ** 2 + (yh - ry) ** 2

    left = central_band & (dl2 >= arc_r * arc_r)
    right = central_band & (dr2 >= arc_r * arc_r)

    if side == "l":
        m = left
    elif side == "r":
        m = right
    else:
        m = left | right

    return m
