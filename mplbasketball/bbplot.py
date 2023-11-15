import numpy as np
import matplotlib.pyplot as plt
from court import Court

nba_court = Court()

fig, ax = nba_court.draw(orientation="h", )
plt.tight_layout()
plt.show()
