from __future__ import annotations

from typing import Literal, Tuple, Sequence

import numpy as np

from .zones import CourtSpec

Half = Literal["l", "r", "u", "d", None]


def get_extent(spec: CourtSpec, half: Half = None) -> Tuple[float, float, float, float]:
    """Return (xmin, xmax, ymin, ymax) for the court in the target orientation.

    For vertical orientation (spec.orientation == 'v'), the coordinate transform is
    (x, y)_v = (-y, x)_h, so the horizontal height maps to vertical x-span.
    """
    w, h = spec.dims

    if spec.orientation == "h":
        cx, cy = spec.center
        xmin, xmax = cx - w / 2.0, cx + w / 2.0
        ymin, ymax = cy - h / 2.0, cy + h / 2.0
        if half == "l":
            xmax = cx
        elif half == "r":
            xmin = cx
        return float(xmin), float(xmax), float(ymin), float(ymax)

    # Vertical: (x, y) -> (-y, x)
    cx, cy = spec.center  # already rotated in CourtSpec.center
    # In vertical coordinates, x-span equals horizontal height (h) and y-span equals horizontal width (w)
    xmin, xmax = cx - h / 2.0, cx + h / 2.0
    ymin, ymax = cy - w / 2.0, cy + w / 2.0
    if half == "d":
        ymax = cy
    elif half == "u":
        ymin = cy
    return float(xmin), float(xmax), float(ymin), float(ymax)


def court_meshgrid(
    spec: CourtSpec, bins: Sequence[int] | int = (50, 50), half: Half = None
) -> Tuple[np.ndarray, np.ndarray]:
    """Return xedges, yedges spanning the court extent for uniform binning.

    bins may be an int (applied to both axes) or a (nx, ny) sequence.
    """
    if isinstance(bins, int):
        nx = ny = bins
    else:
        assert len(bins) == 2, "bins must be int or (nx, ny)"
        nx, ny = int(bins[0]), int(bins[1])
    xmin, xmax, ymin, ymax = get_extent(spec, half)
    xedges = np.linspace(xmin, xmax, nx + 1)
    yedges = np.linspace(ymin, ymax, ny + 1)
    return xedges, yedges


def mask_out_of_bounds(x: np.ndarray, y: np.ndarray, spec: CourtSpec, half: Half = None) -> np.ndarray:
    """Boolean mask of points that fall within the court extent (considering half)."""
    xmin, xmax, ymin, ymax = get_extent(spec, half)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax)


def histogram2d_on_court(
    x: np.ndarray,
    y: np.ndarray,
    spec: CourtSpec,
    bins: Sequence[int] | int = (50, 50),
    half: Half = None,
    weights: np.ndarray | None = None,
    density: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Histogram points using court-aligned uniform bins.

    Returns H, xedges, yedges in the same convention as numpy.histogram2d:
    - H has shape (len(xedges)-1, len(yedges)-1)
    - To plot with pcolormesh, use H.T with xedges, yedges.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xedges, yedges = court_meshgrid(spec, bins=bins, half=half)
    H, xe, ye = np.histogram2d(x, y, bins=[xedges, yedges], weights=weights, density=density)
    return H, xe, ye
