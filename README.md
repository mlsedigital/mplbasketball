<p>
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/mplbb_logo.png" width="50%">
</p>

**A Python plotting library to visualize basketball data, created by the Sport Performance Lab (SPL) at Maple Leaf Sports & Entertainment (MLSE), Toronto, Canada.**

[Sport Performance Lab (SPL)](https://www.mlsedigital.com/innovation-initiatives/sport-performance-lab) is a Research and Development group that works across all MLSE teams on strategic research initiatives in sports analytics and player performance.

# Quick start

Install the package using `pip` (or `pip3`).

```
pip install mplbasketball
```

Plot an NBA basketball court, with the origin at center court, and measuring in feet (currently `"ft"` and `"m"` are supported):

```python
from mplbasketball import Court

court = Court(court_type="nba", origin="center", units="ft")
fig, ax = court.draw(showaxis=True)
```

<p align="center">
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/center_h.png" width=75%>
</p>

Plot some points on the court:

```python
import numpy as np

n_points = 100
x = np.random.uniform(-47, 47, size=n_points)
y = np.random.uniform(-25, 25, size=n_points)

ax.scatter(x, y)
```

<p align="center">
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/center_h_populated.png" width="75%">
</p>

# List of capabilities

Currently, you can use `mplbasketball` to

1. Plot 2D and 3D spatio-temporal basketball data from 4 major basketball competitions
   1. [NBA](https://official.nba.com/rule-no-1-court-dimensions-equipment/)
   2. [WNBA](https://www.wnba.com/archive/wnba/analysis/rule_one.html)
   3. [NCAA](https://ncaaorg.s3.amazonaws.com/championships/sports/basketball/rules/common/PRXBB_CourtDiagram.pdf)
   4. [FIBA](https://nz.basketball/wp-content/uploads/2020/02/FIBA-Basketball-Court-Dimensions.pdf)
2. View data in different orientations orientation (horizontal, vertical, and also normalized to left/right/up/down). The [`utils.transform`](./mplbasketball/utils.py) function makes going between orientations extremely easy and seamless.
3. Easily interface with existing `matplotlib` functions.

# Before you begin

Some notes on plotting data using `mplbasketball`:

1. **Ensure your 2D data is in a right-handed coordinate system (RHCS).** Many data providers (including the [NBA](https://developer.geniussports.com/nbangss/rest/index_central.html#CourtDefinition)) provide their data using left handed coordinate systems (LHCS). If you obtain data in an LHCS, simply flip the sign of all the `y` components (assuming data is left-right), making it compatible with plotting using `mplbasketball`.

# Usage

## The `Court` class

The `Court` class comprises of the dimensions of the basketball court under consideration. When being defined, it takes in a `court_type`, which can currently be `"nba"` (default), `"wnba"`, or `"ncaa"`. Court dimension measurements are provided in `mplbasketball/court_params.py`. The `Court` class has a method `draw()`, which will draw the court in any desired `orientation`:

1. `"h"`: horizontal (default)
2. `"v"`: vertical
3. `"hl"`: horizontal, only left side
4. `"hr"`: horizontal, only right side
5. `"vu"`: vertical, only up side
6. `"vd"`: vertical, only down side

The `draw()` method can either be called to define a matplotlib `fig` and `ax` object using:

```python
from mplbasketball import Court

court = Court(origin="top-left")
fig, ax = court.draw(orientation="h")
```

After this, you can simply plot your data on the `ax` object. **Note that you may need to adjust the `zorder` to ensure all elements are properly visible.**

### Setting the origin

The package allows for the origin of the data to be in 5 locations on the court (numbers quoted below are in feet, and in accordance with the NBA handbook's court dimensions, when using `"m"` as the unit, simply multiply the numbers below by the appropriate conversion factor):

1. `"center"`: Center court and the origin coincide.
2. `"top-left"`: Center court is at `[47, -25]`.
3. `"bottom-left"`: Center court is at `[47, 25]`.
4. `"top-right"`: Center court is at `[-47, -25]`.
5. `"bottom-right"`: Center court is at `[-47, 25]`.

The origin should be specified in the initial specification of the `Court` object. To see what the x and y ranges are for each origin choice, see [this document](https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/docs/origin_vs_coordinates.pdf). **These origin conventions assume the data is in the left-right direction.**

## Transforming Data to Different Orientations

Often, it is more useful to view data from different perspectives. As mentioned in the preceding section, there are 6 orientations to view 2D spatiotemporal data in `mplbasketball`.

Additionally, the `utils.transform()` function allows you to easily change perspectives while accounting for different court types. By selecting a `court_type` (e.g., `"nba"`, `"wnba"`, `"ncaa"`, or `"fiba"`), the function ensures that transformations are accurate for the specific dimensions and characteristics of the chosen court.

We first load some data in its original form; say we are working with a dataset that uses the `"bottom-left"` part of the court as the origin.

```python
import numpy as np
import matplotlib.pyplot as plt
from mplbasketball import Court
from mplbasketball.utils import transform

# Initialize Court object
origin = "bottom-left"
court_type = "nba"
court = Court(origin=origin)
fig, ax = plt.subplots(1, 4)

# Simulate some data
n_pts = 100
x_1 = np.random.uniform(0, 94, size=n_pts)
y_1 = np.random.uniform(0, 50, size=n_pts)

x_2 = np.random.uniform(0, 94, size=n_pts)
y_2 = np.random.uniform(0, 50, size=n_pts)

# On the first subplot, plot the data as is
court.draw(ax[0], )
ax[0].scatter(x_1, y_1, s=5, c="tab:blue")
ax[0].scatter(x_2, y_2, s=5, c="tab:orange")
```

Now, say we want to visualize the first (blue) dataset normalized to the left side, and the second (orange) dataset normalized to the right.
In the second subplot, we can transform the data such that all of the points are normalized to their respective side.

```python
x_1_hl, y_1_hl = transform(x_1, y_1, fr="h", to="hl", origin=origin, court_type=court_type)
x_2_hr, y_2_hr = transform(x_2, y_2, fr="h", to="hr", origin=origin, court_type=court_type)
court.draw(ax[1], )
ax[1].scatter(x_1_hl, y_1_hl, s=5, c="tab:blue")
ax[1].scatter(x_2_hr, y_2_hr, s=5, c="tab:orange")
```

Here, the `fr` and `to` arguments tell the function what orientation the data currently is in, and what the desired orientation is, respectively. Finally, we can visualize this left-normalized data on a vertical court. Say we want to look at the blue data with the hoop at the bottom (the `"vd"` orientation), and the orange data with the hoop at the top. This is again very easy:

```python
x_1_vd, y_1_vd = transform(x_1_hl, y_1_hl, fr="hl", to="vd", origin=origin, court_type=court_type)
court.draw(ax[2], orientation="vd")
ax[2].scatter(x_1_vd, y_1_vd, s=5, c="tab:blue")

x_2_vu, y_2_vu = transform(x_2_hr, y_2_hr, fr="hl", to="vu", origin=origin, court_type=court_type)
court.draw(ax[3], orientation="vu")
ax[3].scatter(x_2_vu, y_2_vu, s=5, c="tab:orange")
```

The final result looks like this:

<p align="center">
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/multi_orientation.png" width="100%">
</p>

Some notes about the above:

1. To produce data for the final plot, we could have also used

```python
x_1_vd, y_1_vd = transform(x_1, y_1, fr="h", to="vd", origin=origin, court_type=court_type)
```

2. To show more/less of the court markings, we can make use of the `zorder` argument in the `ax.scatter` plots.

## 3D Court plotting

The `court3d` module allows for the plotting of 3D basketball data, particularly useful when visualizing 3D ball motion, or in cases where body pose data is available. The `draw_court_3d()` function is the quickest way to obtain a drawing of a court in 3D space.

```python
from mplbasketball.court3d import draw_court_3d
import matplotlib.pyplot as plt

zlim = 20

fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(111, projection="3d")
# Set up initial plot properties
ax.set_zlim([0, zlim])

draw_court_3d(ax, origin=np.array([0.0, 0.0]), line_width=2)
```

<p align="center">
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/court3d.png" width="100%">
</p>

## Interfacing with matplotlib functions

### Hex-binning

```python
import numpy as np
import matplotlib.pyplot as plt
from mplbasketball import Court
from mplbasketball.utils import transform

# Initialize Court object
origin = "bottom-left"
court = Court(origin=origin)
fig, ax = plt.subplots()

# Simulate some data
n_pts = 1000
x_1 = np.random.uniform(0, 94, size=n_pts)
y_1 = np.random.uniform(0, 50, size=n_pts)
x_2 = np.random.uniform(0, 94, size=n_pts)
y_2 = np.random.uniform(0, 50, size=n_pts)

# Transform the data
x_1_hl, y_1_hl = transform(x_1, y_1, fr="h", to="hl", origin=origin,court_type="nba")
x_2_hr, y_2_hr = transform(x_2, y_2, fr="h", to="hr", origin=origin, court_type="nba")

# Draw the court, slightly thicken the lines
court.draw(ax, line_color="white", line_width=0.3)

# Hex-bin the data, while ensuring that the court is plotted on top
ax.hexbin(x_1_hl, y_1_hl, gridsize=(24, 18), extent=(0, 47, 0, 50), zorder=0)
ax.hexbin(x_2_hr, y_2_hr, gridsize=(24, 18), extent=(47, 94, 0, 50), zorder=0 , cmap="hot")
```

<p align="center">
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/hexbin.png" width="75%">
</p>

### Heatmaps

```python
# Compute the heatmap
heatmap_1, xedges_1, yedges_1 = np.histogram2d(x_1, y_1, bins=(94//4, 50//2), range=[[0, 94/2], [0, 50]])
heatmap_2, xedges_2, yedges_2 = np.histogram2d(x_2, y_2, bins=(94//4, 50//2), range=[[94/2, 94], [0, 50]])

# Draw the court, slightly thicken the lines
fig, ax = court.draw(line_color="white", line_width=0.3)

# Display the heatmaps
extent_1 = [xedges_1[0], xedges_1[-1], yedges_1[0], yedges_1[-1]]
extent_2 = [xedges_2[0], xedges_2[-1], yedges_2[0], yedges_2[-1]]

ax.imshow(heatmap_1.T, extent=extent_1, origin='lower', cmap='cividis', zorder=-1)
ax.imshow(heatmap_2.T, extent=extent_2, origin='lower', cmap='cividis', zorder=-1)

```

<p align="center">
  <img src="https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/figs/heatmap.png" width="75%">
</p>

# Documentation

Full documentation coming soon. In the meantime, check out the examples in this README, as well as some of our [examples](https://github.com/mlsedigital/mplbasketball/tree/main/examples)!

# Contribute

We welcome feedback and contributions to this package - browse the [open issues](https://github.com/mlsedigital/mplbasketball/issues), or open a [pull request](https://github.com/mlsedigital/mplbasketball/pulls)!

Please follow the guidelines in our [CONTRIBUTING.md](./CONTRIBUTING.md) file to get started.

# Inspirations

This package takes inspiration from [mplsoccer](https://github.com/andrewRowlinson/mplsoccer), one of the first and best-written sports plotting libraries. Many of the structural decisions made here have been inspired by mplsoccer's `Pitch` class.

# License

[MIT](https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/LICENSE.txt)
