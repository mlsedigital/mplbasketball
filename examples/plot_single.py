import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../")
from court import Court


court_nba = Court(court_type="nba", )
ax = court_nba.draw()

# Add things to plot here, using ax.scatter()

plt.savefig("sample_plot.png")
plt.show()
