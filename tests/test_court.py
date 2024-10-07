# Testing basic 2D court plotting functionality

import matplotlib
import pytest
from mplbasketball import Court

matplotlib.use("Agg")

matplotlib.use("Agg")

@pytest.mark.mpl_image_compare(baseline_dir="baseline")
def test_basic_court_generation():
    """
    Test whether basic court plotting works.
    """
    court = Court(court_type="nba", origin="center", units="ft")
    # Create a new figure
    fig, ax = court.draw(
        orientation="h",
        nrows=1,
        ncols=1,
        dpi=200,
        showaxis=False,
        court_color="none",
        paint_color="none",
        line_color="black",
        line_alpha=1.0,
        line_width=None,
        hoop_alpha=1.0,
        pad=5.0,
    )
    # Add any other basic elements (e.g., player positions)
    ax.scatter([1, 2, 3], [4, 5, 6], color="blue", label="Players")
    # Save the plot to the pytest-mpl baseline
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline")
def test_court_generation_options():
    """
    Test whether basic court plotting works with options.
    """
    court = Court(court_type="nba", origin="center", units="m")
    # Create a new figure
    fig, ax = court.draw(
        orientation="v",
        nrows=1,
        ncols=1,
        dpi=200,
        showaxis=False,
        court_color="gold",
        paint_color="black",
        line_color="white",
        line_alpha=1.0,
        line_width=0.2,
        hoop_alpha=1.0,
        pad=5.0,
    )
    # Add any other basic elements (e.g., player positions)
    # Save the plot to the pytest-mpl baseline
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline")
def test_multiple_plot_generation():
    """
    Test whether basic court plotting works with options.
    """
    court = Court(court_type="nba", origin="center", units="m")
    # Create a new figure
    fig, ax = court.draw(
        orientation="v",
        nrows=2,
        ncols=3,
        dpi=200,
        showaxis=False,
        court_color="none",
        paint_color="none",
        line_color="green",
        line_alpha=1.0,
        line_width=None,
        hoop_alpha=1.0,
        pad=5.0,
    )
    # Add any other basic elements (e.g., player positions)
    # Save the plot to the pytest-mpl baseline
    return fig
