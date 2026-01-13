import numpy as np

from mplbasketball import (
    CourtSpec,
    restricted_area_mask,
    paint_mask,
    corner_three_mask,
    above_break_three_mask,
)


def _h2v(x, y):
    return -y, x


def test_restricted_area_mask_h_and_v_consistency():
    spec_h = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="h")
    spec_v = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="v")

    (lx, ly), (rx, ry) = spec_h.hoop_centers
    r = spec_h.params["charge_circle_radius"]

    # Points near left hoop: one inside (in front), one outside (behind)
    xin = np.array([lx + 0.5 * r])
    yin = np.array([ly])
    xout = np.array([lx - 0.5 * r])
    yout = np.array([ly])

    m_in_h = restricted_area_mask(xin, yin, spec_h, side="l")
    m_out_h = restricted_area_mask(xout, yout, spec_h, side="l")

    assert m_in_h[0]
    assert not m_out_h[0]

    # Rotate to vertical and expect same classification
    xin_v, yin_v = _h2v(xin, yin)
    xout_v, yout_v = _h2v(xout, yout)

    m_in_v = restricted_area_mask(xin_v, yin_v, spec_v, side="l")
    m_out_v = restricted_area_mask(xout_v, yout_v, spec_v, side="l")

    assert m_in_v[0]
    assert not m_out_v[0]


def test_paint_and_corner_masks_basic():
    spec = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="h")
    p = spec.params
    w, h = spec.dims
    cx, cy = spec.center

    # Left paint center point should be inside paint
    outer_w, outer_h = p["outer_paint_dims"]
    xl0 = cx - w / 2.0
    yl0 = cy - outer_h / 2.0
    x_paint = xl0 + outer_w / 2.0
    y_paint = yl0 + outer_h / 2.0

    m_paint = paint_mask(np.array([x_paint]), np.array([y_paint]), spec, side="l")
    assert m_paint[0]

    # Top-left corner three sample should be inside corner mask
    line_len = p["three_point_line_length"]
    side_w = p["three_point_side_width"]
    x_corner = xl0 + line_len / 2.0
    y_corner = cy + h / 2.0 - side_w / 2.0

    m_corner = corner_three_mask(np.array([x_corner]), np.array([y_corner]), spec, side="l")
    assert m_corner[0]


def test_above_break_excludes_corners_and_inside_arc():
    spec = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="h")
    p = spec.params
    w, h = spec.dims
    cx, cy = spec.center
    (lx, ly), _ = spec.hoop_centers

    arc_r = p["three_point_arc_diameter"] / 2.0
    side_w = p["three_point_side_width"]

    # A point outside arc in central band should be in above-break three (left side)
    x_above = lx + arc_r + 1.0
    y_above = cy  # central band
    m_above = above_break_three_mask(np.array([x_above]), np.array([y_above]), spec, side="l")
    assert m_above[0]

    # A point within corner band should not be in above-break
    x_corner_band = cx  # any x, but within corner y-band
    y_corner_band = cy + h / 2.0 - side_w / 2.0
    m_not_above_corner = above_break_three_mask(
        np.array([x_corner_band]), np.array([y_corner_band]), spec, side="l"
    )
    assert not m_not_above_corner[0]

    # A point inside the arc (but central band) should not be in above-break
    x_inside_arc = lx + arc_r - 1.0
    y_inside_arc = cy
    m_not_above_arc = above_break_three_mask(
        np.array([x_inside_arc]), np.array([y_inside_arc]), spec, side="l"
    )
    assert not m_not_above_arc[0]
