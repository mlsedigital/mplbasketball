from matplotlib.colors import LinearSegmentedColormap, ListedColormap


raptors_retro = LinearSegmentedColormap.from_list("raptors_retro", ["#ffffff", "#fe0032", "#ba0c2f", "#9a2271", "#743cc0", "#000000"][::-1])
raptors_brand = LinearSegmentedColormap.from_list("raptors_retro", ["#ffffff", "#888b8d", "#ba0c2f", "#932780", "#743cc0", "#000000"][::-1])
doppler = LinearSegmentedColormap.from_list("doppler", ["#ff0000", "#fd8230", "#fff500", "#67cb5e", "#0085ff", "#0656a0"][::-1])
complimentary = LinearSegmentedColormap.from_list("complimentary", ["#fffee2", "#fff500", "#e4cf12", "#da7920", "#8816bd", "#2e0343"][::-1])
hotcold = LinearSegmentedColormap.from_list("hotcold", ["#ff8c8c", "#ff0000", "#94386b", "#0085ff", "#00407b",][::-1])