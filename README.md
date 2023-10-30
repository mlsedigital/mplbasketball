# mplbasketball
Basketball plotting library for use with matplotlib. Currently a `Court()` object can be defined with an NBA or WNBA court. 

The current iteration of the code only works with Hawk-Eye data. 
- The origin of the coordinate system is at center-court. This means that in-court actions all take place between `[-47, 47]` in the `x` direction, and `[-25, 25]` in the `y` direction. 

See the `examples` folder to get a sense of some examples. We can make plots with single courts, or ones like this:
<img src="./examples/sample_plot.png">

## TO DO

1. Vertical half court plots. 

2. Heat maps.