import numpy as np


class SpatialData():
    """
    A class to handle and manipulate spatial data related to basketball courts.

    The class assumes that the spatial data is input in the 'left-right' direction, with
    the bench-side out-of-bounds line on top. It provides functionalities for standardizing,
    normalizing, and transforming this spatial data based on court orientation and other parameters.

    Attributes:
        x (np.array): The x-coordinates of the spatial data points.
        y (np.array): The y-coordinates of the spatial data points.
        court (Court): An instance of the Court class representing the basketball court.
        origin (str): The origin point of the spatial data, defaults to 'center'.
        lhcs (bool): A flag indicating if the data should be in a left-handed coordinate system.

    Methods:
        get_data(): Returns the x and y coordinates as a tuple.
        standardize(): Standardizes the data based on the coordinate system.
        normalize_side(side): Normalizes the data to be oriented towards a specified side ('left' or 'right').
        transform(orientation): Transforms the spatial data to fit various court orientations.

    Args:
        x (np.array): The x-coordinates of the spatial data points.
        y (np.array): The y-coordinates of the spatial data points.
        court (Court): An instance of the Court class representing the basketball court.
        origin (str, optional): The origin point of the spatial data, defaults to 'center'.
        lhcs (bool, optional): If True, the data is in a left-handed coordinate system. Defaults to True.
    """

    def __init__(self, x, y, court, origin="center", lhcs=True):
        self.x = np.copy(x)
        self.y = np.copy(y)
        self.court = court
        self.origin = origin
        self.lhcs = lhcs
        self.standardize()  # Method that is defined within each subclass

    def get_data(self):
        return self.x, self.y

    def standardize(self):
        if self.lhcs:
            self.y *= -1

    def normalize_side(self, side):
        """
        Normalizes the spatial data to be oriented towards a specified side ('left' or 'right').

        Args:
            side (str): The side towards which the data should be oriented. Must be either 'left' or 'right'.

        Returns:
            tuple: A tuple of np.arrays representing the normalized x and y coordinates.

        Raises:
            AssertionError: If the `side` argument is not 'left' or 'right'.
        """
        assert side in ["left", "right"], "Only normalization to 'left' and 'right' is supported."
        x = np.copy(self.x)
        y = np.copy(self.y)
        # Flip about center court point
        if side == "left":
            pxmask = self.x > 0.
            x[pxmask] *= -1
            y[pxmask] *= -1
        elif side == "right":
            mxmask = self.x < 0.
            x[mxmask] *= -1
            y[mxmask] *= -1
        return x, y

    def transform(self, orientation):
        """
        Transforms the spatial data to fit various court orientations.

        Args:
            orientation (str): The desired orientation of the data. Valid values are 'v', 'h', 'hl', 'hr', 'vu', 'vd'.

        Returns:
            tuple: A tuple of np.arrays representing the transformed x and y coordinates.

        Raises:
            AssertionError: If the `orientation` argument is not one of the valid orientations.
        """
        assert orientation in ["v", "h", "hl", "hr", "vu", "vd"]

        if orientation == "v":
            x = np.copy(self.x)
            y = np.copy(self.y)
            return -y, x
        elif orientation == "h":
            x = np.copy(self.x)
            y = np.copy(self.y)
            return x, y
        elif orientation == "hl":
            return self.normalize_side("left")
        elif orientation == "hr":
            return self.normalize_side("right")
        elif orientation == "vu":
            x, y = self.normalize_side("left")
            return y, -x
        elif orientation == "vd":
            x, y = self.normalize_side("right")
            return y, -x


class Hawkeye(SpatialData):
    """
    A subclass of SpatialData, specifically tailored for handling spatial data provided by the Hawkeye system.

    The Hawkeye class inherits from SpatialData and overrides the standardize method to
    accommodate the specific format and origin point of Hawkeye's data. It adapts the spatial
    data to align with a basketball court's dimensions and orientation as per Hawkeye's system.

    The class assumes that the initial data might be in a left-handed coordinate system (lhcs)
    and provides functionality to standardize it based on the origin point, which could be 'top-left'
    or 'center' (inherited from SpatialData).

    Attributes:
        Inherits all attributes from SpatialData.

    Methods:
        standardize(): Overrides the SpatialData standardize method to standardize the data based on Hawkeye's system.

    Args:
        Inherits all arguments from SpatialData.
    """
    def standardize(self):
        # First flip the y axis in case it is a left-handed CS
        self.y *= -1
        if self.origin == "top-left":
            court_x, court_y = self.court.court_parameters["court_dims"]
            self.x -= court_x/2
            self.y += court_y/2


class NBA(SpatialData):
    def standardize(self):
        if self.lhcs:
            self.y *= -1
        court_x, court_y = self.court.court_parameters["court_dims"]
        self.x = self.x/100 * court_x - court_x/2
        self.y = self.y/100 * court_y + court_y/2
