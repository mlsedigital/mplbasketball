import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from mplbasketball.court_params import _get_court_params_in_desired_units


class LineDataUnits(lines.Line2D):
    def __init__(self, *args, **kwargs):
        _lw_data = kwargs.pop("linewidth", 1)
        super().__init__(*args, **kwargs)
        self._lw_data = _lw_data

    def _get_lw(self):
        if self.axes is not None:
            ppd = 72.0 / self.axes.figure.dpi
            trans = self.axes.transData.transform
            return ((trans((1, self._lw_data)) - trans((0, 0))) * ppd)[1]
        else:
            return 1

    def _set_lw(self, lw):
        self._lw_data = lw

    _linewidth = property(_get_lw, _set_lw)


class PatchDataUnits(patches.PathPatch):
    # https://stackoverflow.com/a/42972469/2912349
    def __init__(self, *args, **kwargs):
        _lw_data = kwargs.pop("linewidth", 1)
        super().__init__(*args, **kwargs)
        self._lw_data = _lw_data

    def _get_lw(self):
        if self.axes is not None:
            ppd = 72.0 / self.axes.figure.dpi
            trans = self.axes.transData.transform
            # the line mentioned below
            return ((trans((self._lw_data, self._lw_data)) - trans((0, 0))) * ppd)[1]
        else:
            return 1

    def _set_lw(self, lw):
        self._lw_data = lw

    _linewidth = property(_get_lw, _set_lw)


class Court:
    """
    A class to represent a basketball court and facilitate its plotting.

    Attributes:
    - court_type (str): Type of the court, either 'nba', 'wnba', or 'ncaa'.
    - units (str): Units of the court dimensions, either 'ft' or 'm'.
    - court_parameters (dict): Parameters defining the dimensions and characteristics of the court.
    - origin (np.array): The origin point of the court.

    Methods:
    - draw(ax, orientation, half, nrows, ncols, dpi, showaxis, court_color, paint_color, line_color, line_alpha, line_width, hoop_alpha, pad):
        Draws the basketball court according to specified parameters.

    Args:
    - court_type (str): Specifies the type of basketball court ('nba' or 'wnba'). Defaults to 'nba'.

    Raises:
    - AssertionError: If the provided court_type is not 'nba', 'wnba', or 'ncaa'.
    """

    def __init__(self, court_type="nba", origin="top-left", units="ft"):

        assert court_type in [
            "nba",
            "wnba",
            "ncaa",
        ], "Invalid court_type. Please choose from ['nba', 'wnba', 'ncaa']"
        assert origin in [
            "center",
            "top-left",
            "bottom-left",
            "top-right",
            "bottom-right",
        ], "Invalid origin. Choose from 'center', '(top/bottom)-(left/right)'"
        assert units in ["m", "ft"], "Invalid units. Currently only 'm' and 'ft' are supported"

        self.court_type = court_type
        self.units = units
        self.court_parameters = _get_court_params_in_desired_units(self.court_type, self.units)

        if origin == "center":
            self.origin = np.array([0.0, 0.0])
        elif origin == "top-left":
            self.origin = np.array(
                [
                    -self.court_parameters["court_dims"][0] / 2,
                    self.court_parameters["court_dims"][1] / 2,
                ]
            )
        elif origin == "bottom-left":
            self.origin = np.array(
                [
                    -self.court_parameters["court_dims"][0] / 2,
                    -self.court_parameters["court_dims"][1] / 2,
                ]
            )
        elif origin == "top-right":
            self.origin = np.array(
                [
                    self.court_parameters["court_dims"][0] / 2,
                    self.court_parameters["court_dims"][1] / 2,
                ]
            )
        elif origin == "bottom-right":
            self.origin = np.array(
                [
                    self.court_parameters["court_dims"][0] / 2,
                    -self.court_parameters["court_dims"][1] / 2,
                ]
            )

    def draw(
        self,
        ax=None,
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
    ):
        """
        Draws the basketball court according to specified parameters.

        This method allows customization of the court's appearance and can plot either a full court or half-court in horizontal or vertical orientation.

        Args:
        - ax (matplotlib.axes.Axes, optional): The matplotlib axes to draw on. If None, a new figure and axes are created.
        - orientation (str): Orientation of the court. Defaults to 'h'.
        - nrows (int): Number of rows in the subplot grid. Defaults to 1.
        - ncols (int): Number of columns in the subplot grid. Defaults to 1.
        - dpi (int): Dots per inch for the plot. Defaults to 200.
        - showaxis (bool): Whether to show axis on the plot. Defaults to False.
        - court_color (str): Background color of the court. Defaults to 'none'.
        - paint_color (str): Color of the paint area. Defaults to 'none'.
        - line_color (str): Color of the lines on the court. Defaults to 'black'.
        - line_alpha (float): Transparency of court lines. Defaults to 1.
        - line_width (float): Width of the lines on the court in correct units. Defaults to None.
        - hoop_alpha (float): Transparency of the hoop. Defaults to 1.
        - pad (float): Padding around the court. Defaults to 5.

        Returns:
        - matplotlib.figure.Figure, matplotlib.axes.Axes: The figure and axes objects containing the court plot.

        Raises:
        - AssertionError: If orientation is not 'horizontal' or 'vertical', or if dpi is less than 200.
        """

        assert orientation in [
            "v",
            "h",
            "hl",
            "hr",
            "vu",
            "vd",
        ], "Invalid orientation. Choose 'horizontal' or 'vertical'"
        assert dpi >= 200, "DPI is too low"

        if len(orientation) > 1:
            half = orientation[1]
        else:
            half = None

        if line_width is None:
            if self.units == "ft":
                line_width = 1.0 / 6.0
            elif self.units == "m":
                line_width = 1.0 / 6.0 * 0.3045

        if ax is None:
            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, dpi=dpi)
            if nrows == 1 and ncols == 1:
                if orientation[0] == "h":
                    self._draw_horizontal_court(
                        axs,
                        half,
                        court_color=court_color,
                        paint_color=paint_color,
                        line_color=line_color,
                        line_alpha=line_alpha,
                        line_width=line_width,
                        hoop_alpha=hoop_alpha,
                        pad=pad,
                    )
                elif orientation[0] == "v":
                    self._draw_vertical_court(
                        axs,
                        half,
                        court_color=court_color,
                        paint_color=paint_color,
                        line_color=line_color,
                        line_alpha=line_alpha,
                        line_width=line_width,
                        hoop_alpha=hoop_alpha,
                        pad=pad,
                    )
                if showaxis is False:
                    axs.axis("off")
                axs.set_aspect("equal")
                return fig, axs
            else:
                for ax in axs.flatten():
                    if orientation[0] == "h":
                        self._draw_horizontal_court(
                            ax,
                            half,
                            court_color=court_color,
                            paint_color=paint_color,
                            line_color=line_color,
                            line_alpha=line_alpha,
                            line_width=line_width,
                            hoop_alpha=hoop_alpha,
                            pad=pad,
                        )
                    elif orientation[0] == "v":
                        self._draw_vertical_court(
                            ax,
                            half,
                            court_color=court_color,
                            paint_color=paint_color,
                            line_color=line_color,
                            line_alpha=line_alpha,
                            line_width=line_width,
                            hoop_alpha=hoop_alpha,
                            pad=pad,
                        )
                    if showaxis is False:
                        ax.axis("off")
                    ax.set_aspect("equal")
            return fig, axs
        else:
            if orientation[0] == "h":
                self._draw_horizontal_court(
                    ax,
                    half,
                    court_color=court_color,
                    paint_color=paint_color,
                    line_color=line_color,
                    line_alpha=line_alpha,
                    line_width=line_width,
                    hoop_alpha=hoop_alpha,
                    pad=pad,
                )
            elif orientation[0] == "v":
                self._draw_vertical_court(
                    ax,
                    half,
                    court_color=court_color,
                    paint_color=paint_color,
                    line_color=line_color,
                    line_alpha=line_alpha,
                    line_width=line_width,
                    hoop_alpha=hoop_alpha,
                    pad=pad,
                )
            if showaxis is False:
                ax.axis("off")
            ax.set_aspect("equal")
            return ax

    def _draw_horizontal_court(
        self,
        ax,
        half,
        court_color,
        paint_color,
        line_color,
        line_alpha,
        line_width,
        hoop_alpha,
        pad,
    ):

        origin_shift_x, origin_shift_y = -self.origin
        court_x, court_y = self.court_parameters["court_dims"]
        cf = line_width / 2

        angle_a = 9.7800457882  # Angle 1 for lower FT line
        angle_b = 12.3415314172  # Angle 2 for lower FT line

        if half is None:
            ax.set_xlim(origin_shift_x - court_x / 2 - pad, origin_shift_x + court_x / 2 + pad)
            ax.set_ylim(origin_shift_y - court_y / 2 - pad, origin_shift_y + court_y / 2 + pad)
        elif half == "l":
            ax.set_xlim(origin_shift_x - court_x / 2 - pad, origin_shift_x + cf)
            ax.set_ylim(origin_shift_y - court_y / 2 - pad, origin_shift_y + court_y / 2 + pad)
        elif half == "r":
            ax.set_xlim(origin_shift_x - cf, origin_shift_x + court_x / 2 + pad)
            ax.set_ylim(origin_shift_y - court_y / 2 - pad, origin_shift_y + court_y / 2 + pad)

        # Draw the main court rectangle
        self._draw_rectangle(
            ax,
            origin_shift_x - court_x / 2 - cf,
            origin_shift_y - court_y / 2 - cf,
            court_x + 2 * cf,
            court_y + 2 * cf,
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            face_color=court_color,
            alpha=line_alpha,
        )

        # Draw the outer paint areas
        outer_paint_x, outer_paint_y = self.court_parameters["outer_paint_dims"]
        # Left side
        if half is None or half == "l":
            self._draw_rectangle(
                ax,
                origin_shift_x - court_x / 2 - cf,
                origin_shift_y - outer_paint_y / 2 - cf,
                outer_paint_x + 2 * cf,
                outer_paint_y + 2 * cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color=paint_color,
                alpha=line_alpha,
            )
        # Right side
        if half is None or half == "r":
            self._draw_rectangle(
                ax,
                origin_shift_x + court_x / 2 - outer_paint_x - cf,
                origin_shift_y - outer_paint_y / 2 - cf,
                outer_paint_x + 2 * cf,
                outer_paint_y + 2 * cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color=paint_color,
                alpha=line_alpha,
            )

        inner_paint_x, inner_paint_y = self.court_parameters["inner_paint_dims"]

        # Draw the hoops
        left_hoop_x = (
            origin_shift_x - court_x / 2 + self.court_parameters["hoop_distance_from_edge"]
        )
        right_hoop_x = (
            origin_shift_x + court_x / 2 - self.court_parameters["hoop_distance_from_edge"]
        )
        # Left side
        if half is None or half == "l":
            self._draw_circle(
                ax,
                left_hoop_x,
                origin_shift_y,
                self.court_parameters["hoop_diameter"],
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color="none",
                alpha=hoop_alpha,
            )
        # Right side
        if half is None or half == "r":
            self._draw_circle(
                ax,
                right_hoop_x,
                origin_shift_y,
                self.court_parameters["hoop_diameter"],
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color="none",
                alpha=hoop_alpha,
            )
        # Draw the backboards
        bb_distance = self.court_parameters["backboard_distance_from_edge"]
        bb_width = self.court_parameters["backboard_width"]
        # Left side
        if half is None or half == "l":
            self._draw_line(
                ax,
                origin_shift_x - court_x / 2 + bb_distance,
                origin_shift_y - bb_width / 2,
                0.0,
                bb_width,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=hoop_alpha,
            )
        # Right side
        if half is None or half == "r":
            self._draw_line(
                ax,
                origin_shift_x + court_x / 2 - bb_distance,
                origin_shift_y - bb_width / 2,
                0.0,
                bb_width,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=hoop_alpha,
            )

        # Draw charge circles
        charge_diameter = 2 * self.court_parameters["charge_circle_radius"]
        # Left side
        if half is None or half == "l":
            self._draw_circular_arc(
                ax,
                left_hoop_x,
                origin_shift_y,
                charge_diameter + cf,
                angle=0,
                theta1=-90,
                theta2=90,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Right side
        if half is None or half == "r":
            self._draw_circular_arc(
                ax,
                right_hoop_x,
                origin_shift_y,
                charge_diameter + cf,
                angle=0,
                theta1=90,
                theta2=-90,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw the free throw arcs
        # Left-upper
        if half is None or half == "l":
            self._draw_circular_arc(
                ax,
                origin_shift_x - court_x / 2 + inner_paint_x + cf,
                origin_shift_y,
                inner_paint_y + 2 * cf,
                angle=0,
                theta1=-90,
                theta2=90,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            # # Left-lower
            if self.court_type in ["nba", "wnba"]:
                # Draw the first arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    origin_shift_x - court_x / 2 + inner_paint_x + cf,
                    origin_shift_y,
                    inner_paint_y + 2 * cf,
                    angle=0,
                    theta1=90,
                    theta2=90 + angle_a,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

                # Draw 13 arcs of angle 'b'
                for i in range(12):
                    start_angle = 90 + angle_a + i * angle_b
                    end_angle = start_angle + angle_b
                    color = line_color if i % 2 == 1 else paint_color

                    self._draw_circular_arc(
                        ax,
                        origin_shift_x - court_x / 2 + inner_paint_x + cf,
                        origin_shift_y,
                        inner_paint_y + 2 * cf,
                        angle=0,
                        theta1=start_angle,
                        theta2=end_angle,
                        line_width=line_width,
                        line_color=color,
                        line_style="-",
                        alpha=line_alpha,
                    )

                # Draw the final arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    origin_shift_x - court_x / 2 + inner_paint_x + cf,
                    origin_shift_y,
                    inner_paint_y + 2 * cf,
                    angle=0,
                    theta1=90 + angle_a + 13 * angle_b,
                    theta2=-90,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

        # Right side
        if half is None or half == "r":
            # Right-lower
            if self.court_type in ["nba", "wnba"]:
                # Draw the first arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    origin_shift_x + court_x / 2 - inner_paint_x - cf,
                    origin_shift_y,
                    inner_paint_y + 2 * cf,
                    angle=180,
                    theta1=90,
                    theta2=90 + angle_a,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

                # Draw 13 arcs of angle 'b'
                for i in range(12):
                    start_angle = 90 + angle_a + i * angle_b
                    end_angle = start_angle + angle_b
                    color = line_color if i % 2 == 1 else paint_color

                    self._draw_circular_arc(
                        ax,
                        origin_shift_x + court_x / 2 - inner_paint_x - cf,
                        origin_shift_y,
                        inner_paint_y + 2 * cf,
                        angle=180,
                        theta1=start_angle,
                        theta2=end_angle,
                        line_width=line_width,
                        line_color=color,
                        line_style="-",
                        alpha=line_alpha,
                    )

                # Draw the final arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    origin_shift_x + court_x / 2 - inner_paint_x - cf,
                    origin_shift_y,
                    inner_paint_y + 2 * cf,
                    angle=180,
                    theta1=90 + angle_a + 13 * angle_b,
                    theta2=-90,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

            # Right-upper
            self._draw_circular_arc(
                ax,
                origin_shift_x + court_x / 2 - inner_paint_x - cf,
                origin_shift_y,
                inner_paint_y + 2 * cf,
                angle=0,
                theta1=90,
                theta2=-90,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw inbound lines
        ib_line_distance = self.court_parameters["inbound_line_distance_from_edge"]
        ib_line_length = self.court_parameters["inbound_line_length"]
        ob_line_distance = self.court_parameters["outbound_line_distance_from_center"]
        ob_line_length = self.court_parameters["outbound_line_length"]
        # Left side
        if half is None or half == "l":
            self._draw_line(
                ax,
                origin_shift_x - court_x / 2 + ib_line_distance + cf,
                origin_shift_y + court_y / 2,
                0.0,
                -ib_line_length + cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                origin_shift_x - court_x / 2 + ib_line_distance + cf,
                origin_shift_y - court_y / 2,
                0.0,
                ib_line_length - cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                origin_shift_x - ob_line_distance,
                origin_shift_y + court_y / 2 + cf,
                0.0,
                ob_line_length - cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Right side
        if half is None or half == "r":
            self._draw_line(
                ax,
                origin_shift_x + court_x / 2 - ib_line_distance + cf,
                origin_shift_y + court_y / 2,
                0.0,
                -ib_line_length + cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                origin_shift_x + court_x / 2 - ib_line_distance + cf,
                origin_shift_y - court_y / 2,
                0.0,
                ib_line_length - cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                origin_shift_x + ob_line_distance,
                origin_shift_y + court_y / 2 + cf,
                0.0,
                ob_line_length - cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw three point areas
        # Draw the arcs arcs
        arc_diameter = self.court_parameters["three_point_arc_diameter"] - line_width / 2
        arc_angle = self.court_parameters["three_point_arc_angle"]
        # Left arc
        if half is None or half == "l":
            self._draw_circular_arc(
                ax,
                left_hoop_x,
                origin_shift_y,
                arc_diameter - 2 * cf,
                angle=0,
                theta1=-arc_angle,
                theta2=arc_angle,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Right arc
        if half is None or half == "r":
            self._draw_circular_arc(
                ax,
                right_hoop_x,
                origin_shift_y,
                arc_diameter - 2 * cf,
                angle=180.0,
                theta1=-arc_angle,
                theta2=arc_angle,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Draw the side lines
        line_length_3pt = self.court_parameters["three_point_line_length"]
        side_width_3pt = self.court_parameters["three_point_side_width"]
        # Left-upper side
        if half is None or half == "l":
            self._draw_line(
                ax,
                origin_shift_x - court_x / 2,
                origin_shift_y + court_y / 2 - side_width_3pt - cf,
                line_length_3pt,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            # Left-lower side
            self._draw_line(
                ax,
                origin_shift_x - court_x / 2,
                origin_shift_y - court_y / 2 + side_width_3pt + cf,
                line_length_3pt,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        if half is None or half == "r":
            # Right-upper side
            self._draw_line(
                ax,
                origin_shift_x + court_x / 2 - line_length_3pt,
                origin_shift_y + court_y / 2 - side_width_3pt - cf,
                line_length_3pt,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            # Right-lower side
            self._draw_line(
                ax,
                origin_shift_x + court_x / 2 - line_length_3pt,
                origin_shift_y - court_y / 2 + side_width_3pt + cf,
                line_length_3pt,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw center line
        self._draw_line(
            ax,
            origin_shift_x,
            origin_shift_y - court_y / 2,
            0.0,
            court_y,
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            alpha=line_alpha,
        )

        # Draw the center circles
        # Outer circle
        self._draw_circle(
            ax,
            origin_shift_x,
            origin_shift_y,
            self.court_parameters["outer_circle_diameter"],
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            face_color=paint_color,
            alpha=line_alpha,
        )
        # Inner circle
        self._draw_circle(
            ax,
            origin_shift_x,
            origin_shift_y,
            self.court_parameters["inner_circle_diameter"],
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            face_color=paint_color,
            alpha=line_alpha,
        )

    def _draw_vertical_court(
        self,
        ax,
        half,
        court_color,
        paint_color,
        line_color,
        line_alpha,
        line_width,
        hoop_alpha,
        pad,
    ):

        court_x, court_y = self.court_parameters["court_dims"]
        origin_shift_x, origin_shift_y = -self.origin

        angle_a = 9.7800457882  # Angle 1 for lower FT line
        angle_b = 12.3415314172  # Angle 2 for lower FT line

        cf = line_width / 2

        if half is None:
            ax.set_ylim(origin_shift_x - court_x / 2 - pad, origin_shift_x + court_x / 2 + pad)
            ax.set_xlim(-origin_shift_y - court_y / 2 - pad, -origin_shift_y + court_y / 2 + pad)
        elif half == "d":
            ax.set_ylim(origin_shift_x - court_x / 2 - pad, origin_shift_x + cf)
            ax.set_xlim(-origin_shift_y - court_y / 2 - pad, -origin_shift_y + court_y / 2 + pad)
        elif half == "u":
            ax.set_ylim(origin_shift_x - cf, origin_shift_x + court_x / 2 + pad)
            ax.set_xlim(-origin_shift_y - court_y / 2 - pad, -origin_shift_y + court_y / 2 + pad)

        # Draw the main court rectangle
        self._draw_rectangle(
            ax,
            -origin_shift_y - court_y / 2 - cf,
            origin_shift_x - court_x / 2 - cf,
            court_y + 2 * cf,
            court_x + 2 * cf,
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            face_color=court_color,
            alpha=line_alpha,
        )

        # Draw the outer paint areas
        outer_paint_x, outer_paint_y = self.court_parameters["outer_paint_dims"]
        # Left side
        if half is None or half == "d":
            self._draw_rectangle(
                ax,
                -origin_shift_y - outer_paint_y / 2 - cf,
                origin_shift_x - court_x / 2 - cf,
                outer_paint_y + 2 * cf,
                outer_paint_x + 2 * cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color=paint_color,
                alpha=line_alpha,
            )
        # Right side
        if half is None or half == "u":
            self._draw_rectangle(
                ax,
                -origin_shift_y - outer_paint_y / 2 - cf,
                origin_shift_x + court_x / 2 - outer_paint_x - cf,
                outer_paint_y + 2 * cf,
                outer_paint_x + 2 * cf,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color=paint_color,
                alpha=line_alpha,
            )

        inner_paint_x, inner_paint_y = self.court_parameters["inner_paint_dims"]

        # Draw the hoops
        left_hoop_x = (
            origin_shift_x - court_x / 2 + self.court_parameters["hoop_distance_from_edge"]
        )
        right_hoop_x = (
            origin_shift_x + court_x / 2 - self.court_parameters["hoop_distance_from_edge"]
        )
        # Left side
        if half is None or half == "d":
            self._draw_circle(
                ax,
                -origin_shift_y,
                left_hoop_x,
                self.court_parameters["hoop_diameter"],
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color="none",
                alpha=hoop_alpha,
            )
        # Right side
        if half is None or half == "u":
            self._draw_circle(
                ax,
                -origin_shift_y,
                right_hoop_x,
                self.court_parameters["hoop_diameter"],
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                face_color="none",
                alpha=hoop_alpha,
            )

        # Draw the backboards
        bb_distance = self.court_parameters["backboard_distance_from_edge"]
        bb_width = self.court_parameters["backboard_width"]
        # Left side
        if half is None or half == "d":
            self._draw_line(
                ax,
                -origin_shift_y - bb_width / 2,
                origin_shift_x - court_x / 2 + bb_distance,
                bb_width,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=hoop_alpha,
            )
        # Right side
        if half is None or half == "u":
            self._draw_line(
                ax,
                -origin_shift_y - bb_width / 2,
                origin_shift_x + court_x / 2 - bb_distance,
                bb_width,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=hoop_alpha,
            )

        # Draw charge circles
        charge_diameter = 2 * self.court_parameters["charge_circle_radius"]
        # Left side
        if half is None or half == "d":
            self._draw_circular_arc(
                ax,
                -origin_shift_y,
                left_hoop_x,
                charge_diameter + cf,
                angle=0,
                theta1=0,
                theta2=180,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Right side
        if half is None or half == "u":
            self._draw_circular_arc(
                ax,
                -origin_shift_y,
                right_hoop_x,
                charge_diameter + cf,
                angle=0,
                theta1=180,
                theta2=0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw the free throw arcs
        # Left-upper
        if half is None or half == "d":
            self._draw_circular_arc(
                ax,
                -origin_shift_y,
                origin_shift_x - court_x / 2 + inner_paint_x + cf,
                inner_paint_y + 2 * cf,
                angle=0,
                theta1=0,
                theta2=180,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            # # Left-lower
            if self.court_type in ["nba", "wnba"]:
                # Draw the first arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    -origin_shift_y,
                    origin_shift_x - court_x / 2 + inner_paint_x + cf,
                    inner_paint_y + 2 * cf,
                    angle=90,
                    theta1=90,
                    theta2=90 + angle_a,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

                # Draw 13 arcs of angle 'b'
                for i in range(12):
                    start_angle = 90 + angle_a + i * angle_b
                    end_angle = start_angle + angle_b
                    color = line_color if i % 2 == 1 else paint_color

                    self._draw_circular_arc(
                        ax,
                        -origin_shift_y,
                        origin_shift_x - court_x / 2 + inner_paint_x + cf,
                        inner_paint_y + 2 * cf,
                        angle=90,
                        theta1=start_angle,
                        theta2=end_angle,
                        line_width=line_width,
                        line_color=color,
                        line_style="-",
                        alpha=line_alpha,
                    )

                # Draw the final arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    -origin_shift_y,
                    origin_shift_x - court_x / 2 + inner_paint_x + cf,
                    inner_paint_y + 2 * cf,
                    angle=90,
                    theta1=90 + angle_a + 13 * angle_b,
                    theta2=-90,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

        # Right side
        if half is None or half == "u":
            # Right-lower
            if self.court_type in ["nba", "wnba"]:
                # Draw the first arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    -origin_shift_y,
                    origin_shift_x + court_x / 2 - inner_paint_x - cf,
                    inner_paint_y + 2 * cf,
                    angle=270,
                    theta1=90,
                    theta2=90 + angle_a,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

                # Draw 13 arcs of angle 'b'
                for i in range(12):
                    start_angle = 90 + angle_a + i * angle_b
                    end_angle = start_angle + angle_b
                    color = line_color if i % 2 == 1 else paint_color

                    self._draw_circular_arc(
                        ax,
                        -origin_shift_y,
                        origin_shift_x + court_x / 2 - inner_paint_x - cf,
                        inner_paint_y + 2 * cf,
                        angle=270,
                        theta1=start_angle,
                        theta2=end_angle,
                        line_width=line_width,
                        line_color=color,
                        line_style="-",
                        alpha=line_alpha,
                    )

                # Draw the final arc of angle 'a'
                self._draw_circular_arc(
                    ax,
                    -origin_shift_y,
                    origin_shift_x + court_x / 2 - inner_paint_x - cf,
                    inner_paint_y + 2 * cf,
                    angle=270,
                    theta1=90 + angle_a + 13 * angle_b,
                    theta2=-90,
                    line_width=line_width,
                    line_color=line_color,
                    line_style="-",
                    alpha=line_alpha,
                )

            # Right-upper
            self._draw_circular_arc(
                ax,
                -origin_shift_y,
                origin_shift_x + court_x / 2 - inner_paint_x - cf,
                inner_paint_y + 2 * cf,
                angle=0,
                theta1=180,
                theta2=0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw inbound lines
        ib_line_distance = self.court_parameters["inbound_line_distance_from_edge"]
        ib_line_length = self.court_parameters["inbound_line_length"]
        ob_line_distance = self.court_parameters["outbound_line_distance_from_center"]
        ob_line_length = self.court_parameters["outbound_line_length"]
        # Left side
        if half is None or half == "d":
            self._draw_line(
                ax,
                -origin_shift_y + court_y / 2,
                origin_shift_x - court_x / 2 + ib_line_distance + cf,
                -ib_line_length + cf,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                -origin_shift_y - court_y / 2,
                origin_shift_x - court_x / 2 + ib_line_distance + cf,
                ib_line_length - cf,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                -origin_shift_y - court_y / 2 - cf,
                origin_shift_x - ob_line_distance,
                -ob_line_length + cf,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Right side
        if half is None or half == "u":
            self._draw_line(
                ax,
                -origin_shift_y + court_y / 2,
                origin_shift_x + court_x / 2 - ib_line_distance + cf,
                -ib_line_length + cf,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                -origin_shift_y - court_y / 2,
                origin_shift_x + court_x / 2 - ib_line_distance + cf,
                ib_line_length - cf,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            self._draw_line(
                ax,
                -origin_shift_y - court_y / 2 - cf,
                origin_shift_x + ob_line_distance,
                -ob_line_length + cf,
                0.0,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw three point areas
        # Draw the arcs arcs
        arc_diameter = self.court_parameters["three_point_arc_diameter"] - line_width / 2
        arc_angle = self.court_parameters["three_point_arc_angle"]
        # Left arc
        if half is None or half == "d":
            self._draw_circular_arc(
                ax,
                -origin_shift_y,
                left_hoop_x,
                arc_diameter - 2 * cf,
                angle=0,
                theta1=90 - arc_angle,
                theta2=90 + arc_angle,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Right arc
        if half is None or half == "u":
            self._draw_circular_arc(
                ax,
                -origin_shift_y,
                right_hoop_x,
                arc_diameter - 2 * cf,
                angle=180.0,
                theta1=90 - arc_angle,
                theta2=arc_angle + 90,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
        # Draw the side lines
        line_length_3pt = self.court_parameters["three_point_line_length"]
        side_width_3pt = self.court_parameters["three_point_side_width"]
        if half is None or half == "d":
            # Left-upper side
            self._draw_line(
                ax,
                -origin_shift_y + court_y / 2 - side_width_3pt - cf,
                origin_shift_x - court_x / 2,
                0.0,
                line_length_3pt,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

            # Left-lower side
            self._draw_line(
                ax,
                -origin_shift_y - court_y / 2 + side_width_3pt + cf,
                origin_shift_x - court_x / 2,
                0.0,
                line_length_3pt,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        if half is None or half == "u":
            # Right-upper side
            self._draw_line(
                ax,
                -origin_shift_y + court_y / 2 - side_width_3pt - cf,
                origin_shift_x + court_x / 2 - line_length_3pt,
                0.0,
                line_length_3pt,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )
            # Right-lower side
            self._draw_line(
                ax,
                -origin_shift_y - court_y / 2 + side_width_3pt + cf,
                origin_shift_x + court_x / 2 - line_length_3pt,
                0.0,
                line_length_3pt,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Draw center line
        self._draw_line(
            ax,
            -origin_shift_y - court_y / 2,
            origin_shift_x,
            court_y,
            0.0,
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            alpha=line_alpha,
        )

        # Draw the center circles

        # Outer circle
        self._draw_circle(
            ax,
            -origin_shift_y,
            origin_shift_x,
            self.court_parameters["outer_circle_diameter"],
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            face_color=paint_color,
            alpha=line_alpha,
        )

        # Inner circle
        self._draw_circle(
            ax,
            -origin_shift_y,
            origin_shift_x,
            self.court_parameters["inner_circle_diameter"],
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            face_color=paint_color,
            alpha=line_alpha,
        )

    def _draw_rectangle(
        self, ax, x0, y0, len_x, len_y, line_width, line_color, line_style, face_color, alpha
    ):
        rectangle = patches.Rectangle(
            (x0, y0),
            len_x,
            len_y,
            linewidth=line_width,
            edgecolor=line_color,
            linestyle=line_style,
            facecolor=face_color,
            alpha=alpha,
        )
        path = rectangle.get_path().transformed(rectangle.get_patch_transform())
        pathpatch = PatchDataUnits(
            path,
            facecolor=face_color,
            edgecolor=line_color,
            linewidth=line_width,
            linestyle=line_style,
        )
        ax.add_patch(pathpatch)

    def _draw_line(self, ax, x0, y0, dx, dy, line_width, line_color, line_style, alpha):
        line = LineDataUnits(
            [x0, x0 + dx],
            [y0, y0 + dy],
            linewidth=line_width,
            color=line_color,
            linestyle=line_style,
            alpha=alpha,
        )
        ax.add_line(line)

    def _draw_circle(
        self, ax, x0, y0, diameter, line_width, line_color, line_style, face_color, alpha
    ):
        circle = patches.Circle(
            (x0, y0),
            diameter,
            linewidth=line_width,
            edgecolor=line_color,
            linestyle=line_style,
            facecolor=face_color,
            alpha=alpha,
        )
        path = circle.get_path().transformed(circle.get_patch_transform())
        pathpatch = PatchDataUnits(
            path,
            facecolor=face_color,
            edgecolor=line_color,
            linewidth=line_width,
            linestyle=line_style,
        )
        ax.add_patch(pathpatch)

    def _draw_circular_arc(
        self, ax, x0, y0, diameter, angle, theta1, theta2, line_width, line_color, line_style, alpha
    ):
        circular_arc = patches.Arc(
            (x0, y0),
            diameter,
            diameter,
            angle=angle,
            theta1=theta1,
            theta2=theta2,
            linewidth=line_width,
            edgecolor=line_color,
            ls=line_style,
            alpha=alpha,
        )
        path = circular_arc.get_path().transformed(circular_arc.get_patch_transform())
        pathpatch = PatchDataUnits(
            path, facecolor="none", edgecolor=line_color, linewidth=line_width, linestyle=line_style
        )
        ax.add_patch(pathpatch)
