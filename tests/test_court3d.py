# Testing basic 3D court plotting functionality

import matplotlib.pyplot as plt
import numpy as np
import pytest

from mplbasketball.court3d import draw_court_3d


@pytest.mark.mpl_image_compare(baseline_dir="baseline", tolerance=25)
def test_court_3d():
    zlim = 20

    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111, projection="3d")
    # Set up initial plot properties
    ax.set_zlim([0, zlim])
    # Stabilize the 3D camera to be deterministic across Matplotlib versions
    ax.view_init(elev=30, azim=-60)
    # Fix axis limits to avoid autoscale differences affecting the view box
    ax.set_xlim([-60, 60])
    ax.set_ylim([-30, 30])

    draw_court_3d(ax, origin=np.array([0.0, 0.0]), line_width=2)

    return fig
