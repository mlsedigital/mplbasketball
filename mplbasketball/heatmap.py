import numpy as np
from scipy.stats import binned_statistic_2d
from scipy.ndimage import gaussian_filter
from mplbasketball.design.colormaps import raptors_retro


def heatmap(ax,
            x_data, y_data,
            grid_x=50, grid_y=50,
            cmap=raptors_retro,
            smooth=True, sigma=1.):
    """
    Creates a heatmap on a given Axes object 'ax' using x and y data.

    The heatmap is constructed by binning the x and y data into a grid,
    and then optionally applying a Gaussian filter for smoothing. The final
    heatmap is plotted on the provided Axes object.

    Parameters:
        ax (matplotlib.axes.Axes): The Axes object on which the heatmap will be plotted.
        x_data (array-like): The x-coordinates of the data points.
        y_data (array-like): The y-coordinates of the data points.
        grid_x (int, optional): The number of bins along the x-axis. Default is 50.
        grid_y (int, optional): The number of bins along the y-axis. Default is 50.
        cmap (str, optional): Colormap to be used for the heatmap. Default is 'Reds'.
        smooth (bool, optional): Flag to apply Gaussian smoothing to the heatmap. Default is True.
        sigma (float, optional): The standard deviation for Gaussian kernel. Used if 'smooth' is True. Default is 1.0.

    Returns:
        None: The function does not return any value but plots a heatmap on the given Axes object.
        This will create and display a heatmap with customized bin size, colormap, and smoothing.
    """

    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    plot_extent = np.concatenate((xlims, ylims))
    statistic, _, _, _ = binned_statistic_2d(x_data, y_data, None, 'count', bins=[grid_x, grid_y], range=[xlims, ylims])

    # Apply Gaussian filter for smoothing
    if smooth:
        statistic = gaussian_filter(statistic, sigma=sigma)

    # Now create the heatmap, setting the extent to the dimensions of the basketball court
    ax.imshow(statistic.T, interpolation='nearest', cmap=cmap, extent=plot_extent, origin='lower')
