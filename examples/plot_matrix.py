import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../")
from court import Court

player_names = ["Fred Van Vleet", 
                "Scottie Barnes",
                "OG Anunoby",
                "Pascal Siakam"]

court_nba = Court(court_type="nba", )
x_pts = np.random.uniform(-47, 47, size=(20,))
y_pts = np.random.uniform(-25, 25, size=(20,))
axs = court_nba.draw(nrows=2, ncols=2)

x_pts = np.random.uniform(-47, 47, size=(20,))
y_pts = np.random.uniform(-25, 25, size=(20,))
axs[0, 0].scatter(x=x_pts, y=y_pts, c="tab:blue")
axs[0, 0].set_title(player_names[0])

x_pts = np.random.uniform(-47, 47, size=(20,))
y_pts = np.random.uniform(-25, 25, size=(20,))
axs[0, 1].scatter(x=x_pts, y=y_pts, c="tab:orange")
axs[0, 1].set_title(player_names[1])

x_pts = np.random.uniform(-47, 47, size=(20,))
y_pts = np.random.uniform(-25, 25, size=(20,))
axs[1, 0].scatter(x=x_pts, y=y_pts, c="tab:red")
axs[1, 0].set_title(player_names[2])

x_pts = np.random.uniform(-47, 47, size=(20,))
y_pts = np.random.uniform(-25, 25, size=(20,))
axs[1, 1].scatter(x=x_pts, y=y_pts, c="tab:green")
axs[1, 1].set_title(player_names[3])
plt.tight_layout()
plt.savefig("sample_plot.png")
plt.show()
