import numpy as np
from scipy.stats import binned_statistic_2d
from scipy.ndimage import gaussian_filter


def heatmap(ax,
            x_data, y_data,
            court,
            grid_x=50, grid_y=50,
            orientation="horizontal", half=False,
            cmap="Reds",
            smooth=True, sigma=1.):

    assert orientation in ["horizontal", "vertical"]

    court_x, court_y = court.court_parameters["court_dims"]

    if orientation == "vertical":
        if half is True:
            extent_x = [-court_x/2, 0.]
            extent_y = [-court_y/2, court_y/2]
        else:
            extent_x = [-court_x/2, court_x/2]
            extent_y = [-court_y/2, court_y/2]

    elif orientation == "horizontal":
        if half is True:
            extent_x = [-court_x/2, 0.]
            extent_y = [-court_y/2, court_y/2]
            plot_extent = np.concatenate((extent_x, extent_y))
        else:
            extent_x = [-court_x/2, court_x/2]
            extent_y = [-court_y/2, court_y/2]
            plot_extent = np.concatenate((extent_x, extent_y))
        statistic, x_edge, y_edge, binnumber = binned_statistic_2d(x_data, y_data, None,
                                                                   'count', bins=[grid_x, grid_y],
                                                                   range=[extent_x, extent_y])

    # Apply Gaussian filter for smoothing
    if smooth:
        smoothed_statistic = gaussian_filter(statistic, sigma=sigma)

    # Now create the heatmap, setting the extent to the dimensions of the basketball court
    ax.imshow(smoothed_statistic.T, interpolation='nearest', cmap=cmap,
              extent=plot_extent, origin='lower')
