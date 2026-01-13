import numpy as np

from mplbasketball import CourtSpec, get_extent, court_meshgrid, histogram2d_on_court, mask_out_of_bounds


def test_get_extent_horizontal_and_halves():
    spec = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="h")
    w, h = spec.dims
    cx, cy = spec.center

    xmin, xmax, ymin, ymax = get_extent(spec)
    assert np.isclose(xmin, cx - w / 2.0)
    assert np.isclose(xmax, cx + w / 2.0)
    assert np.isclose(ymin, cy - h / 2.0)
    assert np.isclose(ymax, cy + h / 2.0)

    xmin_l, xmax_l, ymin_l, ymax_l = get_extent(spec, half="l")
    assert np.isclose(xmin_l, cx - w / 2.0)
    assert np.isclose(xmax_l, cx)

    xmin_r, xmax_r, ymin_r, ymax_r = get_extent(spec, half="r")
    assert np.isclose(xmin_r, cx)
    assert np.isclose(xmax_r, cx + w / 2.0)


def test_get_extent_vertical_and_halves():
    spec = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="v")
    w, h = spec.dims
    cx, cy = spec.center  # already rotated

    xmin, xmax, ymin, ymax = get_extent(spec)
    assert np.isclose(xmax - xmin, h)
    assert np.isclose(ymax - ymin, w)

    xmin_d, xmax_d, ymin_d, ymax_d = get_extent(spec, half="d")
    assert np.isclose(ymax_d, (ymin + ymax) / 2.0)

    xmin_u, xmax_u, ymin_u, ymax_u = get_extent(spec, half="u")
    assert np.isclose(ymin_u, (ymin + ymax) / 2.0)


def test_histogram2d_on_court_shapes_and_bounds():
    spec = CourtSpec(court_type="nba", units="ft", origin="top-left", orientation="h")
    rng = np.random.default_rng(0)
    xedges, yedges = court_meshgrid(spec, bins=(10, 8))

    # Sample random points within extent
    xmin, xmax, ymin, ymax = get_extent(spec)
    xs = rng.uniform(xmin, xmax, size=2000)
    ys = rng.uniform(ymin, ymax, size=2000)

    H, xe, ye = histogram2d_on_court(xs, ys, spec, bins=(10, 8))
    assert H.shape == (len(xedges) - 1, len(yedges) - 1)
    assert np.allclose(xe, xedges)
    assert np.allclose(ye, yedges)

    # Mask out-of-bounds
    m = mask_out_of_bounds(xs, ys, spec)
    assert m.dtype == bool
    assert m.shape == xs.shape
    assert m.sum() == xs.size  # all within bounds
