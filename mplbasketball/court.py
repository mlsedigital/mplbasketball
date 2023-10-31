import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from mplbasketball import court_params


class LineDataUnits(lines.Line2D):
    def __init__(self, *args, **kwargs):
        _lw_data = kwargs.pop("linewidth", 1) 
        super().__init__(*args, **kwargs)
        self._lw_data = _lw_data

    def _get_lw(self):
        if self.axes is not None:
            ppd = 72./self.axes.figure.dpi
            trans = self.axes.transData.transform
            return ((trans((1, self._lw_data))-trans((0, 0)))*ppd)[1]
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
            ppd = 72./self.axes.figure.dpi
            trans = self.axes.transData.transform
            # the line mentioned below
            return ((trans((self._lw_data, self._lw_data))-trans((0, 0)))*ppd)[1]
        else:
            return 1

    def _set_lw(self, lw):
        self._lw_data = lw

    _linewidth = property(_get_lw, _set_lw)


class Court():
    """
    Class for basketball court plotting.
    """

    def __init__(self,
                 provider="hawkeye", court_type="nba",
                 court_color="white",
                 line_color="black", line_alpha=1.0,
                 line_width_in_data_units=1./6.,
                 line_width_in_pts=None,
                 paint_color="none",
                 show_hoop=True, hoop_linewidth=1./6., hoop_color="black", hoop_alpha=1.0,
                 pad=5., axis=False,
                 ):

        assert court_type in ["nba", "wnba"], "Invalid court_type. Please choose from [nba, wnba]"
        assert line_width_in_data_units is None or line_width_in_pts is None, "You cannot specify line width in both points and data units"

        self.provider = provider
        self.court_type = court_type
        self.court_color = court_color
        self.line_color = line_color
        self.line_alpha = line_alpha
        if line_width_in_pts is None:
            self.line_width = line_width_in_data_units
        elif line_width_in_data_units is None:
            self.line_width = line_width_in_pts
        self.paint_color = paint_color
        self.show_hoop = show_hoop
        self.hoop_linewidth = hoop_linewidth
        self.hoop_color = line_color
        self.hoop_alpha = hoop_alpha
        self.pad = pad
        self.axis = axis
        if court_type == "nba":
            self.court_parameters = court_params.nba_court_parameters
        elif court_type == "wnba":
            self.court_parameters = court_params.wnba_court_parameters

    def draw(self, ax=None, figsize=None, nrows=1, ncols=1, dpi=300):
        if ax is None:
            if figsize is None:
                figsize = (12, 6.5)
            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
            if (nrows == 1) and (ncols == 1):
                axs = np.array([axs])
            for ax in axs.flatten():
                self._draw_court(ax)
                ax.set_aspect("equal")
            for ax in axs.flatten():
                self._draw_court(ax)
                ax.set_aspect("equal")
            return axs
        else:
            self._draw_court(ax)
            ax.set_aspect("equal")


    def _draw_court(self, ax):

        court_x, court_y = self.court_parameters["court_dims"]
        ax.set_xlim(-court_x/2-self.pad, court_x/2+self.pad)
        ax.set_ylim(-court_y/2-self.pad, court_y/2+self.pad)

        cf = self.line_width/2

        # Draw the main court rectangle
        self._draw_rectangle(ax, -court_x/2-cf, -court_y/2-cf,
                             court_x+2*cf, court_y+2*cf,
                             line_width=self.line_width,
                             line_color=self.line_color,
                             line_style="-",
                             face_color=self.court_color,
                             alpha=self.line_alpha)

        # Draw the outer paint areas
        outer_paint_x, outer_paint_y = self.court_parameters["outer_paint_dims"]
        # Left side
        self._draw_rectangle(ax, -court_x/2-cf, -outer_paint_y/2-cf,
                             outer_paint_x+2*cf, outer_paint_y+2*cf,
                             line_width=self.line_width,
                             line_color=self.line_color,
                             line_style="-",
                             face_color=self.paint_color,
                             alpha=self.line_alpha)
        # Right side
        self._draw_rectangle(ax, court_x/2-outer_paint_x-cf, -outer_paint_y/2-cf,
                             outer_paint_x+2*cf, outer_paint_y+2*cf,
                             line_width=self.line_width,
                             line_color=self.line_color,
                             line_style="-",
                             face_color=self.paint_color,
                             alpha=self.line_alpha)

        # Draw the inner paint areas
        inner_paint_x, inner_paint_y = self.court_parameters["inner_paint_dims"]
        # Left side
        self._draw_rectangle(ax, -court_x/2-cf, -inner_paint_y/2-cf,
                             inner_paint_x+2*cf, inner_paint_y+2*cf,
                             line_width=self.line_width,
                             line_color=self.line_color,
                             line_style="-",
                             face_color="none",
                             alpha=self.line_alpha)
        # Right side
        self._draw_rectangle(ax, court_x/2-inner_paint_x-cf, -inner_paint_y/2-cf,
                             inner_paint_x+2*cf, inner_paint_y+2*cf,
                             line_width=self.line_width,
                             line_color=self.line_color,
                             line_style="-",
                             face_color="none",
                             alpha=self.line_alpha)

        # Draw the hoops
        left_hoop_x = -court_x/2 + self.court_parameters["hoop_distance_from_edge"] 
        right_hoop_x = court_x/2 - self.court_parameters["hoop_distance_from_edge"]
        # Left side
        self._draw_circle(ax, left_hoop_x, 0.,
                          self.court_parameters["hoop_diameter"],
                          line_width=self.hoop_linewidth,
                          line_color=self.hoop_color,
                          line_style="-",
                          face_color="none",
                          alpha=self.hoop_alpha)
        # Right side
        self._draw_circle(ax, right_hoop_x, 0.,
                          self.court_parameters["hoop_diameter"],
                          line_width=self.hoop_linewidth,
                          line_color=self.hoop_color,
                          line_style="-",
                          face_color="none",
                          alpha=self.hoop_alpha)
        # Draw the backboards
        bb_distance = self.court_parameters["backboard_distance_from_edge"]
        bb_width = self.court_parameters["backboard_width"]
        # Left side
        self._draw_line(ax,
                        -court_x/2+bb_distance, -bb_width/2,
                        0., bb_width,
                        line_width=self.hoop_linewidth,
                        line_color=self.hoop_color,
                        line_style="-",
                        alpha=self.hoop_alpha)
        # Right side
        self._draw_line(ax,
                        court_x/2-bb_distance, -bb_width/2,
                        0., bb_width,
                        line_width=self.hoop_linewidth,
                        line_color=self.hoop_color,
                        line_style="-",
                        alpha=self.hoop_alpha)

        # Draw the free throw arcs
        # Left-upper
        self._draw_circular_arc(ax, -court_x/2+inner_paint_x+cf, 0.,
                                inner_paint_y+2*cf,
                                angle=0, theta1=-90, theta2=90,
                                line_width=self.line_width,
                                line_color=self.line_color,
                                line_style="-",
                                alpha=self.line_alpha)
        # Left-lower
        self._draw_circular_arc(ax, -court_x/2+inner_paint_x+cf, 0.,
                                inner_paint_y+2*cf,
                                angle=0, theta1=90, theta2=-90,
                                line_width=self.line_width,
                                line_color=self.line_color,
                                line_style="--",
                                alpha=self.line_alpha)
        # Right-lower
        self._draw_circular_arc(ax, court_x/2-inner_paint_x-cf, 0.,
                                inner_paint_y+2*cf,
                                angle=0, theta1=-90, theta2=90,
                                line_width=self.line_width,
                                line_color=self.line_color,
                                line_style="--",
                                alpha=self.line_alpha)
        # Right-upper
        self._draw_circular_arc(ax, court_x/2-inner_paint_x-cf, 0.,
                                inner_paint_y+2*cf,
                                angle=0, theta1=90, theta2=-90,
                                line_width=self.line_width,
                                line_color=self.line_color,
                                line_style="-",
                                alpha=self.line_alpha)

        # Draw three point areas
        # Draw the arcs arcs
        arc_diameter = self.court_parameters["three_point_arc_diameter"] - self.line_width/2
        arc_angle = self.court_parameters["three_point_arc_angle"]
        # Left arc
        self._draw_circular_arc(ax, left_hoop_x, 0.,
                                arc_diameter-2*cf,
                                angle=0, theta1=-arc_angle, theta2=arc_angle,
                                line_width=self.line_width,
                                line_color=self.line_color,
                                line_style="-",
                                alpha=self.line_alpha)
        # Right arc
        self._draw_circular_arc(ax, right_hoop_x, 0.,
                                arc_diameter-2*cf,
                                angle=180., theta1=-arc_angle, theta2=arc_angle,
                                line_width=self.line_width,
                                line_color=self.line_color,
                                line_style="-",
                                alpha=self.line_alpha)
        # Draw the side lines
        line_length_3pt = self.court_parameters["three_point_line_length"]
        side_width_3pt = self.court_parameters["three_point_side_width"]
        # Left-upper side
        self._draw_line(ax,
                        -court_x/2, court_y/2-side_width_3pt-cf,
                        line_length_3pt, 0.,
                        line_width=self.line_width,
                        line_color=self.line_color,
                        line_style="-",
                        alpha=self.line_alpha)
        # Right-upper side
        self._draw_line(ax,
                        court_x/2-line_length_3pt, court_y/2-side_width_3pt-cf,
                        line_length_3pt, 0.,
                        line_width=self.line_width,
                        line_color=self.line_color,
                        line_style="-",
                        alpha=self.line_alpha)
        # Left-lower side
        self._draw_line(ax,
                        -court_x/2, -court_y/2+side_width_3pt+cf,
                        line_length_3pt, 0.,
                        line_width=self.line_width,
                        line_color=self.line_color,
                        line_style="-",
                        alpha=self.line_alpha)
        # Right-lower side
        self._draw_line(ax,
                        court_x/2-line_length_3pt, -court_y/2+side_width_3pt+cf,
                        line_length_3pt, 0.,
                        line_width=self.line_width,
                        line_color=self.line_color,
                        line_style="-",
                        alpha=self.line_alpha)

        # Draw center line
        self._draw_line(ax,
                        0., -court_y/2,
                        0., court_y,
                        line_width=self.line_width,
                        line_color=self.line_color,
                        line_style="-",
                        alpha=self.line_alpha)

        # Draw the center circles
        # Inner circle
        self._draw_circle(ax, 0., 0.,
                          self.court_parameters["inner_circle_diameter"],
                          line_width=self.line_width,
                          line_color=self.line_color,
                          line_style="-",
                          face_color=self.paint_color,
                          alpha=self.line_alpha)
        # Outer circle
        self._draw_circle(ax, 0., 0.,
                          self.court_parameters["outer_circle_diameter"],
                          line_width=self.line_width,
                          line_color=self.line_color,
                          line_style="-",
                          face_color=self.paint_color,
                          alpha=self.line_alpha)

        if not self.axis:
            ax.axis("off")

    def _draw_rectangle(self, ax,
                        x0, y0,
                        len_x, len_y,
                        line_width,
                        line_color,
                        line_style,
                        face_color,
                        alpha):
        rectangle = patches.Rectangle((x0, y0),
                                      len_x, len_y,
                                      linewidth=line_width,
                                      edgecolor=line_color,
                                      linestyle=line_style,
                                      facecolor=face_color,
                                      alpha=alpha)
        # ax.add_patch(rectangle)
        path = rectangle.get_path().transformed(rectangle.get_patch_transform())
        pathpatch = PatchDataUnits(path, facecolor=face_color, edgecolor=line_color, linewidth=line_width, linestyle=line_style)
        ax.add_patch(pathpatch)

    def _draw_line(self, ax,
                   x0, y0,
                   dx, dy,
                   line_width,
                   line_color,
                   line_style,
                   alpha):
        line = LineDataUnits([x0, x0+dx], [y0, y0+dy],
                             linewidth=line_width,
                             color=line_color,
                             linestyle=line_style,
                             alpha=alpha)
        ax.add_line(line)
        # line = lines.Line2D([x0, x0+dx], [y0, y0+dy],
        #                     linewidth=line_width,
        #                     color=line_color,
        #                     linestyle=line_style,
        #                     alpha=alpha)
        # ax.add_line(line)

    def _draw_circle(self, ax,
                     x0, y0,
                     diameter,
                     line_width,
                     line_color,
                     line_style,
                     face_color,
                     alpha):
        circle = patches.Circle((x0, y0),
                                diameter,
                                linewidth=line_width,
                                edgecolor=line_color,
                                linestyle=line_style,
                                facecolor=face_color,
                                alpha=alpha)
        # ax.add_patch(circle)
        path = circle.get_path().transformed(circle.get_patch_transform())
        pathpatch = PatchDataUnits(path, facecolor=face_color, edgecolor=line_color, linewidth=line_width, linestyle=line_style)
        ax.add_patch(pathpatch)

    def _draw_circular_arc(self, ax,
                           x0, y0,
                           diameter,
                           angle, theta1, theta2,
                           line_width,
                           line_color,
                           line_style,
                           alpha):
        circular_arc = patches.Arc((x0, y0),
                                   diameter,
                                   diameter,
                                   angle=angle, theta1=theta1, theta2=theta2,
                                   linewidth=line_width,
                                   edgecolor=line_color,
                                   ls=line_style,
                                   alpha=alpha)
        # ax.add_patch(circular_arc)
        path = circular_arc.get_path().transformed(circular_arc.get_patch_transform())
        pathpatch = PatchDataUnits(path, facecolor='none', edgecolor=line_color, linewidth=line_width, linestyle=line_style)
        ax.add_patch(pathpatch)
