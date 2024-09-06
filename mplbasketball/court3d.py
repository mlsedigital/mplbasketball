import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from mplbasketball.court_params import _get_court_params_in_desired_units


class Court3D:
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

    def __init__(self, court_type="nba", origin=np.array([0.0, 0.0]), units="ft"):

        assert court_type in ["nba", "wnba"], "Invalid court_type. Please choose from [nba, wnba]"
        assert units in ["ft", "m"], "Invalid units. Please choose from ['ft', 'm']"

        self.court_type = court_type
        self.units = units
        self.court_parameters = _get_court_params_in_desired_units(self.court_type, self.units)
        self.origin = origin

    def draw(
        self,
        ax,
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
        - line_width (float): Width of the lines on the court. Defaults to 1/6.
        - hoop_alpha (float): Transparency of the hoop. Defaults to 1.
        - pad (float): Padding around the court. Defaults to 5.

        Returns:
            matplotlib.figure.Figure, matplotlib.axes.Axes: The figure and axes objects containing the court plot.

        Raises:
            AssertionError: If orientation is not 'horizontal' or 'vertical', or if dpi is less than 200.
        """

        if line_width is None:
            if self.units == "ft":
                line_width = 1.0 / 6.0
            elif self.units == "m":
                line_width = 1.0 / 6.0 * 0.3048

        self._draw_horizontal_court(
            ax,
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
        self, ax, court_color, paint_color, line_color, line_alpha, line_width, hoop_alpha, pad
    ):

        angle_a = 9.7800457882  # Angle 1 for lower FT line
        angle_b = 12.3415314172  # Angle 2 for lower FT line

        origin_shift_x, origin_shift_y = -self.origin
        court_x, court_y = self.court_parameters["court_dims"]
        cf = 0.0  # line_width/2

        # Draw the main court rectangle
        self._draw_rectangle(
            ax,
            origin_shift_x - court_x / 2 - cf,
            origin_shift_y - court_y / 2,
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

        # Draw the inner paint areas
        inner_paint_x, inner_paint_y = self.court_parameters["inner_paint_dims"]

        # Draw charge circles
        charge_diameter = 2 * self.court_parameters["charge_circle_radius"]
        left_hoop_x = (
            origin_shift_x - court_x / 2 + self.court_parameters["hoop_distance_from_edge"]
        )
        right_hoop_x = (
            origin_shift_x + court_x / 2 - self.court_parameters["hoop_distance_from_edge"]
        )
        # Left side
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
        self._draw_circular_arc(
            ax,
            right_hoop_x,
            origin_shift_y,
            charge_diameter + cf,
            angle=180,
            theta1=-90,
            theta2=90,
            line_width=line_width,
            line_color=line_color,
            line_style="-",
            alpha=line_alpha,
        )

        # Draw the free throw arcs
        # Left-upper
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
        # Left-lower
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
                theta2=270,
                line_width=line_width,
                line_color=line_color,
                line_style="-",
                alpha=line_alpha,
            )

        # Right side
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
                theta2=270,
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
            angle=180,
            theta1=-90,
            theta2=90,
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
        arc_diameter = self.court_parameters["three_point_arc_diameter"] - 0.15
        arc_angle = self.court_parameters["three_point_arc_angle"]
        # Left arc
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
        ax.add_patch(rectangle)

    def _draw_line(self, ax, x0, y0, dx, dy, line_width, line_color, line_style, alpha):
        line = lines.Line2D(
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
        ax.add_patch(circle)

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
        # path = circular_arc.get_path().transformed(circular_arc.get_patch_transform())
        # pathpatch = PatchDataUnits(path, facecolor='none', edgecolor=line_color, linewidth=line_width, linestyle=line_style)
        ax.add_patch(circular_arc)


def draw_court_3d(
    ax3d,
    showaxis=False,
    court_type="nba",
    units="ft",
    court_color="none",
    paint_color="none",
    line_color="black",
    line_alpha=1.0,
    line_width=2,
    hoop_color="black",
    hoop_alpha=1.0,
    pad=5.0,
    origin=np.array([0.0, 0.0]),
):

    fig2d, ax2d = plt.subplots()
    court = Court3D(court_type=court_type, origin=origin, units=units)
    court.draw(
        ax2d,
        showaxis=showaxis,
        court_color=court_color,
        paint_color=paint_color,
        line_color=line_color,
        line_alpha=line_alpha,
        line_width=line_width,
        hoop_alpha=hoop_alpha,
        pad=pad,
    )

    # Draw the hoop and backboard line at the appropriate height
    origin_shift_x, origin_shift_y = -court.origin
    court_x, court_y = court.court_parameters["court_dims"]

    # Draw the hoops
    left_hoop_x = origin_shift_x - court_x / 2 + court.court_parameters["hoop_distance_from_edge"]
    right_hoop_x = origin_shift_x + court_x / 2 - court.court_parameters["hoop_distance_from_edge"]
    # Left side
    left_hoop = patches.Circle(
        (left_hoop_x, origin_shift_y),
        court.court_parameters["hoop_diameter"],
        linewidth=line_width,
        edgecolor=hoop_color,
        linestyle="-",
        alpha=hoop_alpha,
    )

    right_hoop = patches.Circle(
        (right_hoop_x, origin_shift_y),
        court.court_parameters["hoop_diameter"],
        linewidth=line_width,
        edgecolor=hoop_color,
        linestyle="-",
        alpha=hoop_alpha,
    )

    # Draw the backboards
    bb_distance = court.court_parameters["backboard_distance_from_edge"]
    bb_width = court.court_parameters["backboard_width"]
    # Left side
    left_bb = lines.Line2D(
        [origin_shift_x - court_x / 2 + bb_distance, origin_shift_x - court_x / 2 + bb_distance],
        [origin_shift_y - bb_width / 2, origin_shift_y - bb_width / 2 + bb_width],
        linewidth=line_width,
        color=line_color,
        linestyle="-",
        alpha=hoop_alpha,
    )

    right_bb = lines.Line2D(
        [origin_shift_x + court_x / 2 - bb_distance, origin_shift_x + court_x / 2 - bb_distance],
        [origin_shift_y - bb_width / 2, origin_shift_y - bb_width / 2 + bb_width],
        linewidth=line_width,
        color=line_color,
        linestyle="-",
        alpha=hoop_alpha,
    )

    center = left_hoop.center
    radius = left_hoop.radius
    color = left_hoop.get_edgecolor()
    # Create a circle in 3D
    theta = np.linspace(0, 2 * np.pi, 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax3d.plot(x, y, zs=court.court_parameters["hoop_height"], zdir="z", color=hoop_color)

    center = right_hoop.center
    radius = right_hoop.radius
    color = right_hoop.get_edgecolor()
    # Create a circle in 3D
    theta = np.linspace(0, 2 * np.pi, 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax3d.plot(x, y, zs=court.court_parameters["hoop_height"], zdir="z", color=hoop_color)

    x, y = left_bb.get_data()
    ax3d.plot(x, y, zs=court.court_parameters["hoop_height"], zdir="z", color=hoop_color)

    x, y = right_bb.get_data()
    ax3d.plot(x, y, zs=court.court_parameters["hoop_height"], zdir="z", color=hoop_color)

    # For each line in the 2D plot, create a corresponding line in the 3D plot
    for line in ax2d.lines:
        x, y = line.get_data()
        ax3d.plot(x, y, zs=0, zdir="z", color=line.get_color(), lw=line_width)

    # For each patch (like circles), project it onto the 3D plot
    for patch in ax2d.patches:
        if isinstance(patch, mpl.patches.Circle):
            center = patch.center
            radius = patch.radius
            color = patch.get_edgecolor()
            # Create a circle in 3D
            theta = np.linspace(0, 2 * np.pi, 100)
            x = center[0] + radius * np.cos(theta)
            y = center[1] + radius * np.sin(theta)
            ax3d.plot(x, y, zs=0, zdir="z", color=color, lw=line_width)

        elif isinstance(patch, mpl.patches.Rectangle):
            # Project Rectangle
            xy = patch.get_xy()
            width, height = patch.get_width(), patch.get_height()
            rect_x = [xy[0], xy[0], xy[0] + width, xy[0] + width, xy[0]]
            rect_y = [xy[1], xy[1] + height, xy[1] + height, xy[1], xy[1]]
            ax3d.plot(rect_x, rect_y, zs=0, zdir="z", color=patch.get_edgecolor(), lw=line_width)

        elif isinstance(patch, mpl.patches.Arc):
            # Project Arc
            center, width, height = patch.center, patch.width, patch.height
            theta1, theta2, angle = (
                np.radians(patch.theta1),
                np.radians(patch.theta2),
                np.radians(patch.angle),
            )
            theta = np.linspace(angle + theta1, angle + theta2, 100)
            arc_x = center[0] + width / 2.0 * np.cos(theta)
            arc_y = center[1] + height / 2.0 * np.sin(theta)
            ax3d.plot(
                arc_x,
                arc_y,
                zs=0,
                zdir="z",
                color=patch.get_edgecolor(),
                ls=patch.get_linestyle(),
                lw=line_width,
            )

    # Close the temporary figure
    plt.close(fig2d)
